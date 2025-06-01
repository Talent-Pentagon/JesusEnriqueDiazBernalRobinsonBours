import subprocess
import os

def run_test_case(executable_path, input_text, expected_output, test_name, failures):
    result = subprocess.run(
        ['java', '-cp', os.path.dirname(executable_path), os.path.splitext(os.path.basename(executable_path))[0]],
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
            "name": "Alice grades",
            "input": "Alice\n90 80 70 85\n",
            "expected_output": "Student: Alice, Average: 81.25"
        },
        {
            "name": "Bob no grades",
            "input": "Bob\n\n",
            "expected_output": "Student: Bob, Average: 0.00"
        },
        {
            "name": "Charlie one grade",
            "input": "Charlie\n100\n",
            "expected_output": "Student: Charlie, Average: 100.00"
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
    run_tests("./")
