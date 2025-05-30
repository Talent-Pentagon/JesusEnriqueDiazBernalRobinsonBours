import subprocess

def run_test_case(class_name, input_data, expected_output, test_name, failures):
    result = subprocess.run(
        ["java", class_name, input_data],
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

def run_tests(class_name):
    failures = []
    test_cases = [
        ("Fido", "Fido says woof", "Test 1: Fido"),
        ("Max", "Max says woof", "Test 2: Max"),
        ("Doggy", "Doggy says woof", "Test 3: Doggy"),
        ("123", "123 says woof", "Test 4: Numeric name"),
        ("", "Default says woof", "Test 5: Empty name fallback"),
    ]

    for input_data, expected_output, test_name in test_cases:
        run_test_case(class_name, input_data, expected_output, test_name, failures)

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
        print("✅ All Java tests passed.")
        return True

if __name__ == "__main__":
    run_tests("Main")
