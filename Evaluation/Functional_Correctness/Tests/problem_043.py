import subprocess
import os

def run_test_case(executable_path, input_text, expected_output, test_name, failures):
    result = subprocess.run(
        [os.path.abspath(executable_path)],
        input=input_text,
        text=True,
        capture_output=True
    )
    actual_output = result.stdout.strip()
    expected_output = expected_output.strip()

    try:
        assert actual_output == expected_output, \
            f"Expected: '{expected_output}', Got: '{actual_output}'"
    except AssertionError as e:
        failures.append(f"[{test_name}] FAILED: {e}")


def run_tests(executable_path):
    failures = []

    test_cases = [
        {
            "name": "Add + Get",
            "input": "add apple 10\nget apple\nexit\n",
            "expected_output": "10"
        },
        {
            "name": "Add + Restock + Get",
            "input": "add banana 5\nrestock banana 3\nget banana\nexit\n",
            "expected_output": "8"
        },
        {
            "name": "Get Missing Item",
            "input": "get orange\nexit\n",
            "expected_output": "-1"
        }
    ]

    for case in test_cases:
        run_test_case(executable_path, case["input"], case["expected_output"], case["name"], failures)

    print("\n--- TEST RESULTS ---")
    print(f"Total: {len(test_cases)}")
    print(f"Passed: {len(test_cases) - len(failures)}")
    print(f"Failed: {len(failures)}")
    
    if failures:
        print("\n--- FAILURES ---")
        for fail in failures:
            print(fail)
    else:
        print("✅ All tests passed.")


if __name__ == "__main__":
    run_tests("./program.exe") 
