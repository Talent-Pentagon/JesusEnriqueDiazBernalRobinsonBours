import importlib.util
import json
import subprocess
import os


def load_answer(data_model):
        
    test_id = data_model['test_module']
    filename = data_model['filename']
    language = data_model['language']
    return test_id, filename, language

def save_code(code, filename, language):
    ext_map = {"java", "cpp", "c" }
    if language not in ext_map:
        raise ValueError(f"Unsupported language: {language}")

    output_folder = "Model_Answer_Code"
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.join(output_folder, f"{filename}")
    with open(filename, "w") as f:
        f.write(code)
    return 0



def compile_answer(filename, language):
    exe_name = "prog.exe"
    src_file = os.path.join("Model_Answer_Code", filename)
    
    if language == "java":
        compile_proc = subprocess.run(["javac", src_file], capture_output=True, text=True,timeout=10)
        if compile_proc.returncode != 0:
            print(f"Compilation failed: {compile_proc.stderr}")
            return None
        class_name = os.path.splitext(os.path.basename(src_file))[0]
        return class_name


    elif language == "cpp":
        compile_proc = subprocess.run(["g++", src_file, "-o", "prog.exe"], capture_output=True, text=True)
        if compile_proc.returncode != 0:
            print(f"Compilation failed: {compile_proc.stderr}")
            return None
        return exe_name

    elif language == "c":
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


def main():
    file = "resultsBase.json"

    k = int(input("Enter the value of k: "))
    with open(file, "r", encoding='utf-8') as f:
        data_model = json.load(f)
    
    k_passes = 0
    for item in data_model:
        n = 0
        answer_passes = False
        test_id, filename, language = load_answer(item)
        for answer in item['code']:
            save_code(answer, filename, language)
            exe_path = compile_answer(filename, language)
            
            if exe_path is not None:
                run_tests = load_test_runner(test_id)
                results = run_tests(exe_path)  # pass the executable path to test runner             
                if results:
                    answer_passes = True
            n += 1
            if n >= k:
                break

        if answer_passes:
            k_passes += 1
            
        # Calculate Pass@k
        pass_result = k_passes/ len(data_model) if data_model else 0
        print("\nk_passes:", k_passes)  
        print("Total problems:", len(data_model))
        print(f"Pass@{n}: {pass_result:.2%}\n") 

if __name__ == "__main__":
    
    main()

