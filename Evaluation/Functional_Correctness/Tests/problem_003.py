import subprocess
import os

def run_test_case(class_name, input_data, expected_output):
    result = subprocess.run(
        ["java", class_name],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert result.stdout.strip() == expected_output.strip(), f"Expected '{expected_output}', got '{result.stdout.strip()}'"

def run_tests():
    class_name = "Subtract"

    # Test 1
    run_test_case(class_name, "10 5\n", "5")

    # Test 2
    run_test_case(class_name, "20 8\n", "12")

    # Test 3: Negative result
    run_test_case(class_name, "3 9\n", "-6")

    # Test 4: Zero result
    run_test_case(class_name, "7 7\n", "0")

    # Test 5: Negative numbers
    run_test_case(class_name, "-4 -2\n", "-2")

    print("All tests passed.")

if __name__ == "__main__":
    run_tests()
