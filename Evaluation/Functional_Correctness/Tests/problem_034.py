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
            f"Expected:\n'{expected_output}'\nGot:\n'{actual_output}'"
    except AssertionError as e:
        failures.append(f"[{test_name}] FAILED: {e}")

def run_tests(executable_path):
    failures = []

    test_cases = [
        {
            "name": "Basic operations",
            "input": "4\ndeposit 500\nwithdraw 200\nprint\nwithdraw 2000\n",
            "expected_output": "Owner: Alice | Balance: 1300.00\nInsufficient funds"
        },
        {
            "name": "Withdraw exact balance",
            "input": "3\nwithdraw 1000\nprint\ndeposit 100\n",
            "expected_output": "Owner: Alice | Balance: 0.00"
        },
        {
            "name": "Multiple deposits and prints",
            "input": "5\ndeposit 200\nprint\ndeposit 300\nwithdraw 100\nprint\n",
            "expected_output": "Owner: Alice | Balance: 1200.00\nOwner: Alice | Balance: 1400.00"
        },
        {
            "name": "Unknown operation",
            "input": "2\ntransfer 100\nprint\n",
            "expected_output": "Unknown operation: transfer\nOwner: Alice | Balance: 1000.00"
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
        print("Usage: python test_account.py <path_to_executable>")
        sys.exit(1)
    run_tests(sys.argv[1])
