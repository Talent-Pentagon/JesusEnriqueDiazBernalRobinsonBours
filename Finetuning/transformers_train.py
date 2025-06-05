# finetune_unsloth_modal.py

import modal

# --- Define Modal App ---
app = modal.App("transformers-finetuning-v1")

# --- Define the image to install dependencies ---
# We use Modal's GPU image and install unsloth + fastapi + transformers + datasets + trl
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "accelerate",
        "peft",
        "trl",
        "bitsandbytes",
        "datasets",
        "huggingface_hub",
        "hf_transfer",
        "transformers",
        "fastapi",
        "flashinfer-python",
        "vllm",
        "unsloth"
    ).apt_install("git", "cmake", "make", "g++", "libcurl4-openssl-dev", "build-essential", "ccache", "python3-dev", "ninja-build")
)

# --- Define the GPU function ---
@app.function(image=image, gpu="H200", timeout=3600*5, secrets=[modal.Secret.from_name("huggingface")])
@modal.fastapi_endpoint(method="POST")
def run_finetuning():
    from datasets import load_dataset, Dataset, concatenate_datasets
    from itertools import islice
    import os
    import sys, gc, inspect
    from unsloth.chat_templates import standardize_data_formats

    hf_token = os.getenv("HF_TOKEN")

    model_slug = "google/gemma-3-27b-it"  # Change this to your model slug

    import torch

    def clear_cuda_cache():
        """Clear CUDA cache to free up memory."""
        frm = inspect.currentframe().f_back
        caller_locals = frm.f_locals
        caller_globals = frm.f_globals
        for var in ("teacher", "model", "optimizer"):
            if var in caller_locals:
                try:
                    del caller_locals[var]
                    if var in sys.modules:
                        del sys.modules[var]
                except Exception as e:
                    print(f"Error deleting {var}: {e}")
            if var in caller_globals:
                try:
                    del caller_globals[var]
                    if var in sys.modules:
                        del sys.modules[var]
                except Exception as e:
                    print(f"Error deleting {var}: {e}")
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
        gc.collect()
    
    clear_cuda_cache()

    max_seq_length = 8192  # Set the maximum sequence length for the model
    dtype = torch.bfloat16  # Use bfloat16 for better performance on GPUs
    load_in_4bit = False  # Load the model in 4-bit quantization for efficiency
    load_in_8bit = False  # Set to True if you want to load in 8-bit quantization

    from transformers import AutoTokenizer, Gemma3ForCausalLM

    model = Gemma3ForCausalLM.from_pretrained(
        model_slug,
        torch_dtype=dtype,
        device_map="auto",
        token = hf_token,
    )
    model.config.use_cache = False # Disable cache for training

    tokenizer = AutoTokenizer.from_pretrained(model_slug, token = hf_token)
    tokenizer.pad_token = tokenizer.eos_token  # Use eos token as pad token
    tokenizer.padding_side = "right"
    tokenizer.model_max_length = max_seq_length 
    print(tokenizer.padding_side)
    print(tokenizer.pad_token)
    print(tokenizer.special_tokens_map)

    print(model)

    rank = 32
    lora_alpha = 16  # Set LoRA alpha, recommended to be square root of smallest matrix input dimension

    from peft import LoraConfig, get_peft_model

    model = get_peft_model(
        model,
        LoraConfig(
            r=rank,
            lora_alpha=lora_alpha,
            target_modules=[
                "q_proj", 
                "v_proj", 
                "k_proj", 
                "o_proj", 
                #"down_proj"
                ],
            lora_dropout=0.05,
            bias="none",
            modules_to_save=["lm_head", "embed_tokens"],
            use_rslora=True,  # Use RLoRA for better performance
        ),
    )

    model.print_trainable_parameters()

    def load_3k_with_tag(language):
        streamed = load_dataset("ObscuraCoder/ObscuraX", language, split="train", streaming=True)
        samples = list(islice(streamed, 10))
        for s in samples:
            s["lang"] = language
        return Dataset.from_list(samples)

    dataset_c    = load_3k_with_tag("c")
    dataset_cpp  = load_3k_with_tag("cpp")
    dataset_java = load_3k_with_tag("java")
    combined_dataset = concatenate_datasets([dataset_c, dataset_cpp, dataset_java])
    
    new_dataset = []
    for sample in combined_dataset:
        formatted_sample = {
            "conversations": [
                {"content": "Please write some code", "role": "user"},
                {"content": sample["content"], "role": "assistant"}
            ],
            "source": f"{sample['lang']}",
            "score": 4.0
        }
        new_dataset.append(formatted_sample)
    
    dataset = Dataset.from_list(new_dataset)
    dataset = standardize_data_formats(dataset)

    def formatting_prompts_func(examples):
        convos = examples["conversations"]
        texts = [tokenizer.apply_chat_template(convo, tokenize = False, add_generation_prompt = False).removeprefix('<bos>') for convo in convos]
        return { "text" : texts, }

    dataset = dataset.map(formatting_prompts_func, batched = True)

    # print(dataset[100])

    print("Dataset loaded and formatted!")

    print("Starting training...")

    from trl import SFTTrainer, SFTConfig
    from transformers import TrainingArguments, DataCollatorForLanguageModeling
    from transformers import get_scheduler

    per_device_train_batch_size = 1
    gradient_accumulation_steps = 1
    epochs = 1
    learning_rate = 2e-5

    total_steps = len(dataset) // (per_device_train_batch_size * gradient_accumulation_steps) * epochs
    warmup_steps = int(total_steps * 0.1)  # 10% of total steps for warmup
    anneal_start_step = int(total_steps * 0.5)  # Anneal after 50% of steps

    from torch.optim import AdamW
    optimizer = AdamW(model.parameters(), lr=learning_rate, weight_decay=0.01)

    from torch.optim.lr_scheduler import LambdaLR

    def custom_lr_scheduler(optimizer, num_warmup_steps, num_training_steps, anneal_start_step):
        def lr_lambda(current_step):
            if current_step < num_warmup_steps:
                return float(current_step) / float(max(1, num_warmup_steps))
            elif current_step < anneal_start_step:
                return 1.0
            else:
                return max(0.0, float(num_training_steps - current_step) / float(max(1, num_training_steps - anneal_start_step)))
        return LambdaLR(optimizer, lr_lambda)

    scheduler = custom_lr_scheduler(optimizer, warmup_steps, total_steps, anneal_start_step)

    from unsloth import is_bfloat16_supported

    common_args = {
        "per_device_train_batch_size": per_device_train_batch_size,
        "per_device_eval_batch_size": per_device_train_batch_size,
        "gradient_accumulation_steps": gradient_accumulation_steps,
        "num_train_epochs": epochs,
        "logging_strategy": "steps",
        "eval_strategy": "no",
        "logging_steps": 1,
        "bf16": is_bfloat16_supported(),  # Use BF16 if supported
        "fp16": not is_bfloat16_supported(),  # Use FP16 if BF16 is not supported
        "seed": 3407,
        "output_dir": "gemma-3-finetune",
        "gradient_checkpointing": True,  # Enable gradient checkpointing for memory efficiency
        "gradient_checkpointing_kwargs": {"use_reentrant": True},  # Use reentrant checkpointing
        "remove_unused_columns": False,  # Keep all columns in the dataset
    }

    common_args["dataset_num_proc"] = 1  # Use 1 processes for dataset processing
    common_args["max_seq_length"] = 8192  # Max Sequence Length
    common_args["dataset_text_field"] = "text"  # Use 1 processes for dataset processing
    
    distilled = False  # Set to True if using a distilled model
    run_name = "gemma_3_finetuned_model"
    common_args["run_name"] = run_name

    trainer = SFTTrainer(
        model = model,
        processing_class = tokenizer,
        train_dataset = dataset,
        args = SFTConfig(**common_args),
        optimizers = (optimizer, scheduler)
    )

    print(trainer.train_dataset)

    print(tokenizer.chat_template)



    print("Trainer initialized!")
    trainer_stats = trainer.train()

    # Push to Hub (you must set tokens or use secrets)
    
    model = model.merge_and_unload()
    model.save_pretrained(f"{run_name}/")    
    tokenizer.save_pretrained(f"{run_name}/")
    model.push_to_hub(
        repo_id = "GhostMopey115/gemma-finetuned-transformers",
        token = hf_token,
    )
    tokenizer.push_to_hub(
        repo_id = "GhostMopey115/gemma-finetuned-transformers",
        token = hf_token,
    )
    
    # Transform model to gguf format
        # Convert to GGUF using llama.cpp
    import subprocess
    GGUF_OUTPUT_DIR = f"{run_name}/"

    # Clone llama.cpp if not already
    if not os.path.exists("llama.cpp"):
        subprocess.run(["git", "clone", "https://github.com/ggerganov/llama.cpp"], check=True)

    # Build llama.cpp tools
    # subprocess.run(["cmake", "-B", "llama.cpp/build", "-DCMAKE_BUILD_TYPE=Release", "-G", "Ninja"], check=True)
    # subprocess.run(["ninja", "-C", "llama.cpp/build"], check=True)

    # Convert the model to GGUF format
    subprocess.run([
        "python3", "llama.cpp/convert_hf_to_gguf.py",
        f"{run_name}/", 
        "--outtype", "q8_0",  # Use Q8_0 quantization
    ], check=True)

    print(f"Model successfully converted to GGUF format in {GGUF_OUTPUT_DIR}/")

    from huggingface_hub import upload_folder

    repo_id = "GhostMopey115/gemma-finetuned-transformers-gguf"

    # Upload GGUF folder to a subdirectory called "gguf"
    upload_folder(
        repo_id=repo_id,
        folder_path=GGUF_OUTPUT_DIR,
        token=hf_token,
    )