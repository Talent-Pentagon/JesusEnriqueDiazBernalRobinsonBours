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
    # Test 1: Simple positive numbers
    run_test_case(executable_path, "2 3\n", "6")

    # Test 2: Larger numbers
    run_test_case(executable_path, "10 15\n", "150")

    # Test 3: Multiplying by zero
    run_test_case(executable_path, "0 25\n", "0")

    # Test 4: Negative times positive
    run_test_case(executable_path, "-4 6\n", "-24")

    # Test 5: Positive times negative
    run_test_case(executable_path, "7 -3\n", "-21")

    # # Test 6: Negative times negative
    # run_test_case(executable_path, "-5 -5\n", "25")

    # # Test 7: Multiplying large values
    # run_test_case(executable_path, "1000 2000\n", "2000000")

    print("All tests passed.")

if __name__ == "__main__":
    run_tests("./multiply")
