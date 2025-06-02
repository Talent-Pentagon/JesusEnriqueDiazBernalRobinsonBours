import subprocess
import os
import sys

def run_test_case(executable_path, expected_lines, test_name, failures):
    try:
        result = subprocess.run(
            [os.path.abspath(executable_path)],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout.strip()

        for expected in expected_lines:
            if expected not in output:
                failures.append(
                    f"[{test_name}] FAILED: Expected line not found:\n'{expected}'\n--- Output was:\n{output}"
                )
    except Exception as e:
        failures.append(f"[{test_name}] CRASHED: {e}")

def run_tests(executable_path):
    failures = []

    tests = [
        {
            "name": "Flat Discount for 150.0",
            "expected_lines": ["Flat: 135.00"]
        },
        {
            "name": "Seasonal Discount for 150.0",
            "expected_lines": ["Seasonal: 127.50"]
        }
    ]

    for test in tests:
        run_test_case(executable_path, test["expected_lines"], test["name"], failures)

    print("\n--- TEST RESULTS ---")
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {len(tests) - len(failures)}")
    print(f"Failed: {len(failures)}")

    if failures:
        print("\n--- FAILURES ---")
        for fail in failures:
            print(fail)
    else:
        print("✅ All tests passed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_discount.py <path_to_executable>")
        sys.exit(1)
    run_tests(sys.argv[1])
