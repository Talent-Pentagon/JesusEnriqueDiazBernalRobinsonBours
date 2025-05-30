import subprocess
import os

def run_test_case(executable_path, input_data, expected_output, test_name, failures):
    result = subprocess.run(
        ["java", executable_path],  # Java class name only, no .class or .java
        input=input_data,           # Send input via stdin
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
        ("42", "x = 42", "Test 1: Positive number"),
        ("0", "x = 0", "Test 2: Zero"),
        ("-100", "x = -100", "Test 3: Negative number"),
        ("9999", "x = 9999", "Test 4: Large number"),
        ("7", "x = 7", "Test 5: Single digit"),
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
        print("✅ All C tests passed.")
        return True

if __name__ == "__main__":
    run_tests("./c_object")
