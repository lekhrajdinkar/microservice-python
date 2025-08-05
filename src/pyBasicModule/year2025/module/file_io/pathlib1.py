from pathlib import Path
import io

def pathlib_basics():
    print(" ❇️ === Pathlib Basics ===")

    # Current directory
    cwd = Path.cwd()
    print("Current directory:", cwd)

    # Create a new directory
    new_dir = cwd / "demo_pathlib"
    new_dir.mkdir(exist_ok=True)

    # Create a file path
    file_path = new_dir / "example.txt"
    print("File path:", file_path)

    # Write to file
    file_path.write_text("Hello from pathlib!\n")

    # Read from file
    content = file_path.read_text()
    print("File content:", content)

    # File details
    print("Exists?", file_path.exists())
    print("Is file?", file_path.is_file())
    print("Size (bytes):", file_path.stat().st_size)

    # Clean up
    #file_path.unlink()
    #new_dir.rmdir()

def io_basics():
    print("\n=== io Module (In-Memory File) ===")

    # Simulate a file in memory
    mem_file = io.StringIO()
    mem_file.write("In-memory log line 1\n")
    mem_file.write("In-memory log line 2\n")

    # Go to beginning
    mem_file.seek(0)

    # Read line-by-line
    print("Reading memory file:")
    for line in mem_file:
        print(">", line.strip())

    mem_file.close()

def io_binary_example():
    print("\n=== io.BytesIO (Binary In-Memory File) ===")

    # Create binary in-memory file
    bio = io.BytesIO()
    bio.write(b'\x00\x01\x02HelloBinary')

    # Read bytes
    bio.seek(0)
    data = bio.read()
    print("Binary content:", data)

    bio.close()

def pathlib_advanced():
    print("\n=== Pathlib Advanced ===")
    root = Path.cwd()

    # Recursively list all .py files
    print("Python files under current dir:")
    for py_file in root.rglob("*.py"):
        print(py_file)

    # Combine paths safely
    print("Safe join path:", root.joinpath("folder", "file.txt"))

    # Using resolve to get absolute path
    print("Resolved path:", (root / "..").resolve())

# cd C:\Users\Manisha\Documents\GitHub\idea\02-etl-pyspark\src\pyBasicModule\year2025
# python -m module.file_io.pathlib1

if __name__ == "__main__":
    pathlib_basics()
    #io_basics()
    #io_binary_example()
    #pathlib_advanced()
