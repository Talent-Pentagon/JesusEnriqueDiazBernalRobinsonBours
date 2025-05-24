import importlib.util
# from models import base_model, finetuned_model
import json

def load_test_runner(test_path):
    spec = importlib.util.spec_from_file_location("test_module", test_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_tests

# Evaluate the model on a set of problems
# and return the pass rate for each k value
def evaluate_model(model_code, problems, k_values):
    results = {k: 0 for k in k_values}

    for problem in problems:
        desc = problem["description"]
        test_fn = load_test_runner(problem["test_module"])
        all_candidates = model.generate_solutions(desc, num_solutions=max(k_values))

        for k in k_values:
            passed = False
            for code in all_candidates[:k]:
                try:
                    if test_fn(code):
                        passed = True
                        break
                except Exception:
                    continue
            if passed:
                results[k] += 1

    return {k: results[k] / len(problems) for k in k_values}


# Main
if __name__ == "__main__":
    with open("problems.json") as f:
        problems = json.load(f)
        
        
        

    print("Evaluating base model...")
    pass_base = evaluate_model(model_code, problems, k=5) # Change with model answer
    print("Evaluating finetuned model...")
    pass_finetuned = evaluate_model(model_code, problems, k=5) # Change with model answer
    
    # Obtain k pass rates 
    # evaluate_model(my_model, problems, k_values=[1, 3, 5])

    print(f"Base Pass@5: {pass_base:.2%}")
    print(f"Finetuned Pass@5: {pass_finetuned:.2%}")
    
    print(f"Improvement: {((pass_finetuned - pass_base) * 100):.2f}%")
