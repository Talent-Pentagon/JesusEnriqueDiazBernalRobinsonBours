import importlib.util
# from models import base_model, finetuned_model
import json
import subprocess
import os


def load_answer(i, data_problem, data_model):
        
    test_id = data_problem[i]['test_module']
    language = data_problem[i]['language']
    return test_id, language

def save_code(code, test_id, language):
    ext_map = {
        "java": "java",
        "c++": "cpp",
        "c": "c"
    }
    ext = ext_map.get(language)
    if not ext:
        raise ValueError(f"Unsupported language: {language}")

    output_folder = "Model_Answer_Code"
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.join(output_folder, f"{test_id}.{ext}")
    code = code['code']
    with open(filename, "w") as f:
        f.write(code)
    return filename



def compile_answer(filename, language):
    exe_name = "prog.exe"
    
    if language == "java":
        src_file = filename
        compile_proc = subprocess.run(["javac", src_file], capture_output=True, text=True)
        if compile_proc.returncode != 0:
            print(f"Compilation failed: {compile_proc.stderr}")
            return None
        # Return the class name (filename without .java)
        class_name = os.path.splitext(os.path.basename(src_file))[0]
        return class_name


    elif language == "c++":
        src_file = filename
        compile_proc = subprocess.run(["g++", src_file, "-o", "prog.exe"], capture_output=True, text=True)
        if compile_proc.returncode != 0:
            print(f"Compilation failed: {compile_proc.stderr}")
            return None
        return exe_name

    elif language == "c":
        src_file = filename
        compile_proc = subprocess.run(["gcc", src_file, "-o", "prog.exe"], capture_output=True, text=True)
        if compile_proc.returncode != 0:
            print(f"Compilation failed: {compile_proc.stderr}")
            return None
        return exe_name

    else:
        print(f"Unknown language: {language}")
        return None


def load_test_runner(test_id):
    test_path = os.path.join("Tests", f"problem_{test_id}.py")
    spec = importlib.util.spec_from_file_location("test_module", test_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_tests  # function in the test module


def main(problems_path, model_answer_path):
    with open(problems_path, "r") as f:
        data_problem = json.load(f)
    with open(model_answer_path, "r", encoding='utf-8') as f:
        data_model = json.load(f)
        
    i = 0
    for item in data_model:
        test_id, language = load_answer(i, data_problem, data_model)
        
        filename = save_code(item, test_id, language)
        print(filename)
        exe_path = compile_answer(filename, language)
        
        if exe_path is None:
            print("Compilation failed, skipping tests.")
            return
        
        run_tests = load_test_runner(test_id)
        print(f"Running tests for problem {test_id} ...")
        run_tests(exe_path)  # pass the executable path to test runner
        
        i += 1

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python evaluate_passak.py <problems.json> <model_answers.json>")
    else:
        problems_file = sys.argv[1]
        model_output_file = sys.argv[2]
        main(problems_file, model_output_file)

        
        
        

    # print("Evaluating base model...")
    # pass_base = evaluate_model(model_code, problems, k=5) # Change with model answer
    # print("Evaluating finetuned model...")
    # pass_finetuned = evaluate_model(model_code, problems, k=5) # Change with model answer
    
    # # Obtain k pass rates 
    # # evaluate_model(my_model, problems, k_values=[1, 3, 5])

    # print(f"Base Pass@5: {pass_base:.2%}")
    # print(f"Finetuned Pass@5: {pass_finetuned:.2%}")
    
    # print(f"Improvement: {((pass_finetuned - pass_base) * 100):.2f}%")
