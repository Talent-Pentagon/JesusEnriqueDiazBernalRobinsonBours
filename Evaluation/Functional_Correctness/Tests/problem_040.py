import subprocess
import os
import sys

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
            f"Expected:\n'{expected_output}'\nGot:\n'{actual_output}'"
    except AssertionError as e:
        failures.append(f"[{test_name}] FAILED: {e}")

def run_tests(executable_path):
    failures = []

    # Expected output from the current main function
    expected_output = """
Running: Backup Database (Priority 5)
Running: Update Firmware (Priority 2)
Running: Send Logs (Priority 1)
""".strip()

    test_cases = [
        {
            "name": "Default Scheduler Output",
            "expected_output": expected_output
        },
        {
            "name": "Repeat Run",
            "expected_output": expected_output
        }
    ]

    for case in test_cases:
        run_test_case(executable_path, case["expected_output"], case["name"], failures)

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
        print("Usage: python test_scheduler.py <path_to_executable>")
        sys.exit(1)
    run_tests(sys.argv[1])
