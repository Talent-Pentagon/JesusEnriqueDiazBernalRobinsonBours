import subprocess
import os
import sys

def run_test_case_with_input(executable_path, input_lines, expected_lines, test_name, failures):
    try:
        # Prepare input string with newlines
        input_str = "\n".join(input_lines) + "\n\n"  # Double newline may help to stop input reading if needed
        
        # Run the executable, sending input_str to its stdin
        result = subprocess.run(
            [os.path.abspath(executable_path)],
            input=input_str,
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout.strip()

        # Check if each expected line appears in the output
        for expected in expected_lines:
            if expected not in output:
                failures.append(
                    f"[{test_name}] FAILED: Expected line not found:\n'{expected}'\n--- Output was:\n{output}"
                )
    except Exception as e:
        failures.append(f"[{test_name}] CRASHED: {e}")

def run_tests(executable_path):
    failures = []

    # Define test cases:
    tests = [
        {
            "name": "Test 1 - Enqueue 6 messages (overflow)",
            "input_lines": ["Hello", "World", "from", "the", "buffer", "Overflow", ""],  # final empty line to signal input end
            "expected_lines": [
                "Msg: World",
                "Msg: from",
                "Msg: the",
                "Msg: buffer",
                "Msg: Overflow"
            ]
        },
        {
            "name": "Test 2 - Enqueue 3 messages",
            "input_lines": ["One", "Two", "Three", ""],
            "expected_lines": [
                "Msg: One",
                "Msg: Two",
                "Msg: Three"
            ]
        },
        {
            "name": "Test 3 - Enqueue exactly MAX messages",
            "input_lines": ["A", "B", "C", "D", "E", ""],
            "expected_lines": [
                "Msg: A",
                "Msg: B",
                "Msg: C",
                "Msg: D",
                "Msg: E"
            ]
        },
        {
            "name": "Test 4 - Enqueue no messages",
            "input_lines": [""],  # no messages
            "expected_lines": [
                # No output expected, but program may print nothing
            ]
        },
        {
            "name": "Test 5 - Enqueue 7 messages (overflow twice)",
            "input_lines": ["M1", "M2", "M3", "M4", "M5", "M6", "M7", ""],
            "expected_lines": [
                "Msg: M3",
                "Msg: M4",
                "Msg: M5",
                "Msg: M6",
                "Msg: M7"
            ]
        }
    ]

    for test in tests:
        run_test_case_with_input(executable_path, test["input_lines"], test["expected_lines"], test["name"], failures)

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
        print("Usage: python test_queue.py <path_to_executable>")
        sys.exit(1)
    run_tests(sys.argv[1])
