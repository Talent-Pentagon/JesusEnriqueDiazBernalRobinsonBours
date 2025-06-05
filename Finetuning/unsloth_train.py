# finetune_unsloth_modal.py

import modal

# --- Define Modal App ---
app = modal.App("unsloth-finetuning-final-qwen")

# --- Define the image to install dependencies ---
# We use Modal's GPU image and install unsloth + fastapi + transformers + datasets + trl
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "bitsandbytes",  # bitsandbytes does not support --no-deps on pip_install, so keep it here
        "accelerate",
        "xformers==0.0.29.post3",
        "peft",
        "trl==0.15.2",
        "triton",
        "cut_cross_entropy",
        "unsloth_zoo",
        "sentencepiece",
        "protobuf",
        "datasets>=3.4.1",
        "huggingface_hub",
        "hf_transfer",
        "transformers==4.51.3",
        "fastapi",
        "torch",  # ensure PyTorch is installed
        "unsloth",
    ).apt_install("git", "cmake", "make", "g++", "libcurl4-openssl-dev", "build-essential", "ccache")
)

# --- Define the GPU function ---
@app.function(image=image, gpu="H200", timeout=3600*5, secrets=[modal.Secret.from_name("huggingface")])
@modal.fastapi_endpoint(method="POST")
def run_finetuning():
    from unsloth import FastLanguageModel
    import torch
    from datasets import load_dataset, Dataset, concatenate_datasets
    from transformers import TrainingArguments
    from itertools import islice
    import os
    from unsloth.chat_templates import standardize_data_formats
    from unsloth.chat_templates import get_chat_template

    fourbit_models = [
        # 4bit dynamic quants for superior accuracy and low memory use
        "unsloth/gemma-3-1b-it-unsloth-bnb-4bit",
        "unsloth/gemma-3-4b-it-unsloth-bnb-4bit",
        "unsloth/gemma-3-12b-it-unsloth-bnb-4bit",
        "unsloth/gemma-3-27b-it-unsloth-bnb-4bit",

        # Other popular models!
        "unsloth/Llama-3.1-8B",
        "unsloth/Llama-3.2-3B",
        "unsloth/Llama-3.3-70B",
        "unsloth/mistral-7b-instruct-v0.3",
        "unsloth/Phi-4",
    ] # More models at https://huggingface.co/unsloth

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = "unsloth/Qwen3-14B-unsloth-bnb-4bit",
        max_seq_length = 8192, # Choose any for long context!
        load_in_4bit = True,  # 4 bit quantization to reduce memory
        load_in_8bit = False, # [NEW!] A bit more accurate, uses 2x memory
        full_finetuning = False, # [NEW!] We have full finetuning now!
        # token = "hf_...", # use one if using gated models
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r = 64, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj",],
        lora_alpha = 128,
        lora_dropout = 0, # Supports any, but = 0 is optimized
        bias = "none",    # Supports any, but = "none" is optimized
        # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
        use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
        random_state = 3407,
        use_rslora = False,  # We support rank stabilized LoRA
        loftq_config = None, # And LoftQ
    )


    streamed = load_dataset("GhostMopey115/FinalFinetuningDataset", split="train", streaming=True)
    combined_dataset = Dataset.from_list(list(streamed))

    # Filter out a specific class
    combined_dataset = combined_dataset.filter(
        lambda example: example["classification"] != "Procedural"
)
    
    EOS_TOKEN = tokenizer.eos_token

    def formatting_prompts_func(examples):
        return {"text": [c + EOS_TOKEN for c in examples["content"]]}

    # Apply the formatting to the combined dataset
    dataset = combined_dataset.map(formatting_prompts_func, batched=True)

    print("Dataset loaded and formatted!")

    print("Starting training...")



    from trl import SFTTrainer, SFTConfig
    from transformers import TrainingArguments
    from unsloth import is_bfloat16_supported

    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = 8192,
        dataset_num_proc = 1,
        args = TrainingArguments(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,

            # Use num_train_epochs = 1, warmup_ratio for full training runs!
            warmup_steps = 5,
            num_train_epochs = 1,

            learning_rate = 2e-4,
            fp16 = not is_bfloat16_supported(),
            bf16 = is_bfloat16_supported(),
            logging_steps = 1,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
            output_dir = "outputs",
            report_to = "none", # Use this for WandB etc
        ),
    )


    trainer_stats = trainer.train()

    # Push to Hub (you must set tokens or use secrets)
    hf_token = os.getenv("HF_TOKEN")
    model.push_to_hub("GhostMopey115/lora_model_final", token = hf_token) # Online saving
    tokenizer.push_to_hub("GhostMopey115/lora_model_final", token = hf_token) # Online saving

    # model.push_to_hub_gguf("GhostMopey115/model_final", tokenizer, token = hf_token)
    model.push_to_hub_gguf("GhostMopey115/model_16_final", tokenizer, quantization_method = "f16", token = hf_token)
