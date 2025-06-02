import subprocess
import os
import sys

def run_test_case(executable_path, input_text, expected_lines, test_name, failures):
    try:
        result = subprocess.run(
            [os.path.abspath(executable_path)],
            input=input_text,
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
            "name": "Employee Bonus - Bob",
            "input": "Bob 50000 5\n",
            "expected_lines": ["Total Salary with Bonus: 55000"]
        },
        {
            "name": "Employee Bonus - Alice",
            "input": "Alice 60000 2\n",
            "expected_lines": ["Total Salary with Bonus: 62000"]
        },
        {
            "name": "Employee Bonus - Charlie",
            "input": "Charlie 45000 0\n",
            "expected_lines": ["Total Salary with Bonus: 45000"]
        },
        {
            "name": "Employee Bonus - Dana",
            "input": "Dana 30000 10\n",
            "expected_lines": ["Total Salary with Bonus: 40000"]
        },
        {
            "name": "Employee Bonus - Evan",
            "input": "Evan 80000 1\n",
            "expected_lines": ["Total Salary with Bonus: 81000"]
        }
    ]

    for test in tests:
        run_test_case(executable_path, test["input"], test["expected_lines"], test["name"], failures)

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
        print("Usage: python test_employee_bonus.py <path_to_executable>")
        sys.exit(1)
    run_tests(sys.argv[1])
