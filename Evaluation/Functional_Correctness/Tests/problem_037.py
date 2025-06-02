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

    # Your expected output (from the current main function)
    expected_output = """
--- Dinosaur Zoo Info ---
Dinosaur: T-Rex
Age: 68 million years ago
Length: 12.30 meters
Bite Force: 12000 PSI
T-Rex lets out a terrifying, bone-crushing roar!
T-Rex stomps powerfully across the land.
T-Rex devours plants or meat with ferocious appetite.

Dinosaur: Triceratops
Age: 68 million years ago
Length: 9.00 meters
Horn Length: 2 meters
Triceratops makes a deep grunt.
Triceratops walks steadily with heavy steps.
Triceratops grazes peacefully on plants or meat.

Dinosaur: Velociraptor
Age: 75 million years ago
Length: 2.00 meters
Speed: 60 km/h
Velociraptor lets out a high-pitched screech!
Velociraptor runs swiftly at 60 km/h.
Velociraptor quickly scavenges plants or meat.
""".strip()

    test_cases = [
        {
            "name": "Default Zoo Output",
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
        print("Usage: python test_dino_zoo.py <path_to_executable>")
        sys.exit(1)
    run_tests(sys.argv[1])
