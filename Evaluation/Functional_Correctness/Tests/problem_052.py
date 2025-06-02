import subprocess
import os
import sys

def run_test_case(executable_path, arg, expected_lines, test_name, failures):
    try:
        result = subprocess.run(
            [os.path.abspath(executable_path), arg],
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
            "name": "Find Book 1984",
            "arg": "1984",
            "expected_lines": ["Found: 1984 by Orwell"]
        },
        {
            "name": "Find Book Dune",
            "arg": "Dune",
            "expected_lines": ["Found: Dune by Herbert"]
        },
        {
            "name": "Find Book Not Present",
            "arg": "Nonexistent",
            "expected_lines": ["Book not found."]
        }
    ]

    for test in tests:
        run_test_case(executable_path, test["arg"], test["expected_lines"], test["name"], failures)

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
        print("Usage: python test_library.py <path_to_executable>")
        sys.exit(1)
    run_tests(sys.argv[1])
