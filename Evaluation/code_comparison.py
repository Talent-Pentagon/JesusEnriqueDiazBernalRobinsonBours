import wandb
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForCausalLM
import torch
import difflib
import tempfile
import subprocess
import re
import os
import textwrap

wandb.init(project="code-fix-comparison", name="demo-nonfinetuned-vs-finetuned") 

# Model base (no fine-tuned)
model_base_name = "Salesforce/codegen-350M-mono"
tokenizer_base = AutoTokenizer.from_pretrained(model_base_name)
model_base = AutoModelForCausalLM.from_pretrained(model_base_name).to("cuda")

# Modelo fine-tuned (reemplaza por uno fine-tuned real, o usa un modelo distinto)
# Aquí uso el mismo modelo base para simular
model_finetuned_name = "EleutherAI/gpt-neo-125M"  # Cambia a tu fine-tuned
tokenizer_ft = AutoTokenizer.from_pretrained(model_finetuned_name)
model_ft = AutoModelForCausalLM.from_pretrained(model_finetuned_name).to("cuda")

# Código con error para corregir
code_input = """
    def calculate(a, c):
        b = a + "c"   
        return b
        
    def main(),
        result = calculate(5, 10
        print("Result:", result)
"""

def generate_fix(model, tokenizer, input_code, max_length=100):
    inputs = tokenizer(input_code, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_length=max_length, do_sample=False)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded

# Generar salidas
# output_base = generate_fix(model_base, tokenizer_base, code_input)
# output_ft = generate_fix(model_ft, tokenizer_ft, code_input)
output_base = """
import math
Bob = 0
def calculateSum(a, b, c):
    if a > b:
        result = a + b
    elif b > c:
        result = b + c
    else:
        result = a + c
    return result

def processData():
    x = 10
    y = 20
    z = 30
    sum = calculate_sum(x, y, z)
    print("Sum is", sum)
    unused_variable = 42

processData()

"""
output_ft = """
def calculateSum(a: int, b: int, c: int) -> int:
    nums = sorted([a, b, c], reverse=True)
    return nums[0] + nums[1]

def validate_inputs(a: int, b: int, c: int) -> bool:
    return all(isinstance(i, int) and i >= 0 for i in (a, b, c))

def process_data() -> None:
    a, b, c = 15, 5, 10
    if not validate_inputs(a, b, c):
        print("Invalid inputs. Please enter non-negative integers.")
        return

    total = calculateSum(a, b, c)
    if total > 30:
        print("Sum is high:", total)
    elif total > 10:
        print("Sum is moderate:", total)
    else:
        print("Sum is low:", total)

if __name__ == "__main__":
    process_data()

"""


print("=== Output Base ===")
print(output_base)
print("\n=== Output Fine-tuned ===")
print(output_ft)

def count_changes(original, fixed):
    # Use SequenceMatcher to get ratio of similarity
    sm = difflib.SequenceMatcher(None, original, fixed)
    # Ratio is between 0 and 1; 1 means identical
    similarity = sm.ratio()
    # Or get number of different characters/changes:
    opcodes = sm.get_opcodes()
    changes = 0
    for tag, i1, i2, j1, j2 in opcodes:
        if tag != 'equal':
            changes += max(i2 - i1, j2 - j1)
    return changes

# ---------- Helpers for metrics ----------
# Save code to a temporary file
# In your save_temp_code function
def save_temp_code(code: str, suffix=".py") -> str:
    code = textwrap.dedent(code)  # Fix indentation
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode="w", encoding="utf-8")
    tmp_file.write(code)
    tmp_file.close()
    return tmp_file.name


# Run pylint and get score and issues
def run_pylint(file_path):
    result = subprocess.run(["python", "-m", "pylint", file_path, "--exit-zero"], capture_output=True, text=True)
    text = result.stdout
    score_match = re.search(r'Your code has been rated at ([\d\.]+)/10', text)
    score = float(score_match.group(1)) if score_match else 0.0
    issue_lines = [
            line for line in text.splitlines()
            if re.search(r':[0-9]+:[0-9]+: [RCWE][0-9]{4}:', line)
        ]
    return score, len(issue_lines)


# Run Radon to get complexity
def run_radon_complexity(file_path):
    result = subprocess.run(["python", "-m", "radon", "cc", file_path, "-s", "-a"], capture_output=True, text=True)
    output = result.stdout
    match = re.search(r'Average complexity: [A-Z] \(([\d\.]+)\)', output)
    return float(match.group(1)) if match else 0.0


# Count changes
changes_base = count_changes(code_input, output_base)
changes_ft = count_changes(code_input, output_ft)

# Save to temporary files
file_base = save_temp_code(output_base)
file_ft = save_temp_code(output_ft)

# Run Pylint
score_base, issues_base = run_pylint(file_base)
score_ft, issues_ft = run_pylint(file_ft)

# Run Radon
complexity_base = run_radon_complexity(file_base)
complexity_ft = run_radon_complexity(file_ft)

# Clean up temporary files
os.unlink(file_base)
os.unlink(file_ft)

# Crear una tabla
table = wandb.Table(columns=[
    "input_code",
    "output_base",
    "output_compare",
    "changes_base",
    "changes_compare",
    "pylint_score_base",
    "pylint_score_compare",
    "pylint_issues_base",
    "pylint_issues_compare",
    "radon_complexity_base",
    "radon_complexity_compare"
])

# Create a table with relevant metrics for graphing
metrics_table = wandb.Table(columns=[
    "feature", "base", "finetuned"
])

# Log complexity
metrics_table.add_data("radon complexity values", complexity_base, complexity_ft)

# Log pylint issues
metrics_table.add_data("issues found", issues_base, issues_ft)

# Log changes
metrics_table.add_data("changes made", changes_base,changes_ft)

# Log pylint scores
metrics_table.add_data("score value", score_base, score_ft)

# Log table to WandB
wandb.log({"model_metrics_table": metrics_table})


# Log metrics
table = wandb.Table(columns=["input", "output_base", "changes_base", "output_finetuned", "changes_finetuned"])
table.add_data(code_input, output_base, changes_base, output_ft, changes_ft)
wandb.log({"code_comparison": table})

wandb.finish()



