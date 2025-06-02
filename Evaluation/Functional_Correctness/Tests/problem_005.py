import subprocess
import os
import sys

def run_test_case(executable_path, input_data, expected_output, test_name, failures):
    result = subprocess.run(
        [os.path.abspath(executable_path), input_data],
        text=True,
        capture_output=True
    )
    actual_output = result.stdout.strip()
    expected_output = expected_output.strip()

    try:
        assert actual_output == expected_output, \
            f"Expected '{expected_output}', got '{actual_output}'"
    except AssertionError as e:
        failures.append(f"[{test_name}] FAILED: {e}")

def run_tests(executable_path):
    failures = []
    test_cases = [
        ("Tesla", "Model: Tesla", "Test 1: Tesla"),
        ("Honda", "Model: Honda", "Test 2: Honda"),
        ("1234", "Model: 1234", "Test 3: Numeric model"),
        ("Cybertruck", "Model: Cybertruck", "Test 4: Cybertruck"),
        ("A", "Model: A", "Test 5: Single character"),
    ]

    for input_data, expected_output, test_name in test_cases:
        run_test_case(executable_path, input_data, expected_output, test_name, failures)

    total_tests = len(test_cases)
    failed_tests = len(failures)
    passed_tests = total_tests - failed_tests

    print(f"\n--- TEST RESULTS ---")
    print(f"Total: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")

    if failures:
        print("\n--- TEST FAILURES ---")
        for failure in failures:
            print(failure)
        return False
    else:
        print("✅ All C++ tests passed.")
        return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_xyz.py <path_to_executable>")
        sys.exit(1)
    run_tests(sys.argv[1])
