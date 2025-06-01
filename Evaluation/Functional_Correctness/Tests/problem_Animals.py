import subprocess
import os

java_class_dir = os.path.abspath("Model_Answer_Code/Animals")
print(f"Java class path: {java_class_dir}")

def run_test_case(java_class_path, classname, args, expected_output, test_name, failures):

    command = ["java", "-cp", java_class_path, classname]
    if args:
        command.extend(args.split())

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    actual_output = result.stdout.strip()
    expected_output = expected_output.strip()

    if result.returncode != 0 or result.stderr:
        print(f"[{test_name}] Java Error:\n{result.stderr.strip()}")

    try:
        assert actual_output == expected_output, \
            f"Expected: '{expected_output}', Got: '{actual_output}'"
    except AssertionError as e:
        failures.append(f"[{test_name}] FAILED: {e}")


def run_tests(executable_path):
    failures = []

    test_cases = [
        {
            "name": "With Argument",
            "args": "Rover",
            "expected_output": "Rover says woof"
        },
        {
            "name": "Default Name",
            "args": "",
            "expected_output": "Default says woof"
        },
        {
            "name": "Special Characters",
            "args": "D@isy",
            "expected_output": "D@isy says woof"
        },
        {
            "name": "Empty String",
            "args": "\"\"",
            "expected_output": " says woof"
        }
    ]

    for case in test_cases:
        run_test_case(java_class_dir, "Animals", case["args"], case["expected_output"], case["name"], failures)

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
    run_tests("Animals")
