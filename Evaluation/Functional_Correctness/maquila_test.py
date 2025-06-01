import subprocess
import sys
from pathlib import Path

def compile_source(src_path):
    ext = src_path.suffix
    exe_path = src_path.with_name(f"{src_path.stem}.exe")

    if ext == ".c":
        compile_cmd = ["gcc", str(src_path), "-o", str(exe_path)]
    elif ext == ".cpp":
        compile_cmd = ["g++", str(src_path), "-o", str(exe_path)]
    else:
        print(f"❌ Unsupported file type: {ext}")
        sys.exit(1)

    print(f"📦 Compiling {src_path}...")
    result = subprocess.run(compile_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Compilation failed:\n{result.stderr}")
        sys.exit(1)

    print("✅ Compilation succeeded.")
    return exe_path

def run_test(test_script, exe_path):
    print(f"🚀 Running test script: {test_script} with {exe_path}")
    result = subprocess.run(
        [sys.executable, str(test_script), str(exe_path)],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("⚠️ Errors:\n", result.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run_any.py <path_to_code_in_A> <path_to_test_in_B>")
        sys.exit(1)

    src_path = Path(sys.argv[1])
    test_script_path = Path(sys.argv[2])

    if not src_path.exists():
        print(f"❌ Source file not found: {src_path}")
        sys.exit(1)
    if not test_script_path.exists():
        print(f"❌ Test file not found: {test_script_path}")
        sys.exit(1)

    exe_path = compile_source(src_path)
    run_test(test_script_path, exe_path)
