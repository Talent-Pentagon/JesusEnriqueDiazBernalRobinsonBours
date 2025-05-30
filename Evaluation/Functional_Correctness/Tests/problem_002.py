import subprocess
import os

def run_test_case(executable_path, expected_output, test_name, failures):
    result = subprocess.run(
        [os.path.abspath(executable_path)],
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
        ("2", "Test 1: Two increments should return 2"),
    ]

    for expected_output, test_name in test_cases:
        run_test_case(executable_path, expected_output, test_name, failures)

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
    run_tests("./counter")  
