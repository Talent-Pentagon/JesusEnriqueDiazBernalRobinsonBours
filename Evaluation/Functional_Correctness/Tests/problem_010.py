import subprocess
import os
import sys

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
            "name": "Single Employee",
            "input": "John 40 15.0\n",
            "expected_output": "Pay for John: 600.00"
        },
        {
            "name": "Multiple Employees",
            "input": "Alice 35 20.0\nBob 50 18.5\n",
            "expected_output": "Pay for Alice: 700.00\nPay for Bob: 925.00"
        },
        {
            "name": "Zero Hours",
            "input": "Chris 0 25.0\n",
            "expected_output": "Pay for Chris: 0.00"
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
    if len(sys.argv) != 2:
        print("Usage: python test_employee.py <path_to_executable>")
        sys.exit(1)
    run_tests(sys.argv[1])
