import subprocess
import tempfile
import os
from datasets import load_dataset, Dataset, concatenate_datasets
from itertools import islice

def run_analysis(code):
    with tempfile.NamedTemporaryFile(mode='w+', suffix=".txt", delete=False, dir="../data", encoding="utf-8") as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        # Run lexer and parser
        subprocess.run(["../bin/lexer", tmp_path], check=True)
        result = subprocess.run(["../bin/parser"], check=True)
        # Read the output file
        with open("./classification.txt", "r") as f:
            output_lines = f.read().strip().splitlines()

        if len(output_lines) >= 2:
            classification = output_lines[0].strip()
            confiability = output_lines[1].strip()
        else:
            classification = "unknown"
            confiability = "0"

    except subprocess.CalledProcessError as e:
        classification = "error"
        confiability = "0"
        print(f"Error analyzing file {tmp_path}: {e}")
    
    except FileNotFoundError:
        classification = "file_not_found"
        confiability = "0"
        print("Error: classification.txt not found.")

    finally:
        os.remove(tmp_path)

    return classification, confiability

def load_3k_with_tag(language):
    streamed = load_dataset("ObscuraCoder/ObscuraX", language, split="train", streaming=True)
    samples = list(islice(streamed, 1000))
    for s in samples:
        s["lang"] = language
    return Dataset.from_list(samples)

def enrich_dataset(dataset):
    oop = 0
    hy = 0
    pro = 0
    new_samples = []
    for sample in dataset:
        code = sample["content"]
        classification, confiability = run_analysis(code)
        if classification == "OOP":
            oop += 1
        elif classification == "Hibrido":
            hy += 1
        elif classification == "Procedural":
            pro += 1
        sample["classification"] = classification
        sample["confiability"] = confiability
        new_samples.append(sample)
    print(f"Classification counts: oop={oop}, hy={hy}, pro={pro}")
    print(f"Total samples processed: {len(new_samples)}")
    return Dataset.from_list(new_samples)

# Load datasets
dataset_c    = load_3k_with_tag("c")
dataset_cpp  = load_3k_with_tag("cpp")
dataset_java = load_3k_with_tag("java")

# Combine datasets
combined_dataset = concatenate_datasets([dataset_c, dataset_cpp, dataset_java])

# Enrich with classification and confiability
enriched_dataset = enrich_dataset(combined_dataset)

enriched_dataset.to_json("my_dataset.jsonl")

# for sample in enriched_dataset:
#     print(f"Classification: {sample['classification']}, Confiability: {sample['confiability']}")

