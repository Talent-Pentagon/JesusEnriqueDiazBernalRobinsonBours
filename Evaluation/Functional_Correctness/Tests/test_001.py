import subprocess
import json

def test_java(doc_name):
    # Compile the Java program
    proc = subprocess.run(
        ["javac", doc_name],
        capture_output=True, text=True
    )
    assert proc.returncode == 0, f"Compilation failed: {proc.stderr}"

    run = subprocess.run(
        ["java", doc_name],
        input="2 3",
        capture_output=True,
        text=True
    )
    output = run.stdout.strip()
    assert output == "5", f"Expected 5 but got {output}"

def test_cpp():
    proc = subprocess.run(
        ["g++", "001.cpp", "-o", "prog"],
        capture_output=True, text=True
    )
    assert proc.returncode == 0, f"Compilation failed: {proc.stderr}"

    run = subprocess.run(
        ["./prog"],
        input="2 3",
        capture_output=True,
        text=True
    )
    output = run.stdout.strip()
    assert output == "5", f"Expected 5 but got {output}"

def test_c():
    proc = subprocess.run(
        ["gcc", "001.c", "-o", "prog"],
        capture_output=True, text=True
    )
    assert proc.returncode == 0, f"Compilation failed: {proc.stderr}"

    run = subprocess.run(
        ["./prog"],
        input="10 4",
        capture_output=True,
        text=True
    )
    output = run.stdout.strip()
    assert output == "6", f"Expected 6 but got {output}"

# Main
if __name__ == "__main__":
    with open("problems.json") as f:
        problems = json.load(f)
    for item in problems:
        

test_c()
test_cpp()
test_java()