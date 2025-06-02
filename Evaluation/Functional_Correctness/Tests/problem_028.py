import subprocess
import os
import sys

def run_test_case(executable_path, expected_output_snippet, test_name, failures):
    result = subprocess.run(
        [os.path.abspath(executable_path)],
        text=True,
        capture_output=True
    )
    actual_output = result.stdout.strip()

    try:
        assert expected_output_snippet in actual_output, \
            f"Expected output snippet not found.\nExpected:\n'{expected_output_snippet}'\nActual output:\n'{actual_output}'"
    except AssertionError as e:
        failures.append(f"[{test_name}] FAILED: {e}")

def run_tests(executable_path):
    failures = []

    test_cases = [
        {
            "name": "T-Rex info",
            "expected_output": "Name: T-Rex\nAge: 68 million years ago\nLength: 12.30 meters"
        },
        {
            "name": "T-Rex roar",
            "expected_output": "T-Rex lets out a terrifying roar!"
        },
        {
            "name": "Triceratops info",
            "expected_output": "Name: Triceratops\nAge: 68 million years ago\nLength: 9.00 meters"
        },
        {
            "name": "Triceratops roar",
            "expected_output": "Triceratops makes a grunt sound."
        },
        {
            "name": "T-Rex hunt",
            "expected_output": "T-Rex is hunting its prey."
        },
        {
            "name": "Triceratops defend",
            "expected_output": "Triceratops defends itself with its horns."
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
        print("Usage: python test_dinosaur_structs.py <path_to_executable>")
        sys.exit(1)
    run_tests(sys.argv[1])
