import subprocess
import os

def run_test_case(executable_path, input_data, expected_output):
    result = subprocess.run(
        [os.path.abspath(executable_path)],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert result.stdout.strip() == expected_output.strip(), f"Expected '{expected_output}', got '{result.stdout.strip()}'"

def run_tests(executable_path):
    # Test 1
    run_test_case(executable_path, "2 3\n", "5")

    # Test 2
    run_test_case(executable_path, "10 15\n", "25")

    # Test 3: Negative numbers
    run_test_case(executable_path, "-5 -8\n", "-13")

    # Test 4: Zero
    run_test_case(executable_path, "0 0\n", "0")

    # Test 5: Mixed positive and negative
    run_test_case(executable_path, "-7 4\n", "-3")

    print("All tests passed.")

if __name__ == "__main__":
    run_tests("./add")
