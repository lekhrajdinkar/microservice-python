"""
| Category         | Common Use                               | Example Function                          |
| ---------------- | ---------------------------------------- | ----------------------------------------- |
| Basic            | Get working directory, list files        | `os.getcwd()`, `os.listdir()`             |
| File Ops         | Create, rename, delete files/directories | `os.rename()`, `os.remove()`              |
| Path Handling    | Join, split, absolute path               | `os.path.join()`, `os.path.abspath()`     |
| Metadata         | Size, modification time                  | `os.path.getsize()`, `os.path.getmtime()` |
| Environment Vars | Get/set env vars                         | `os.environ`, `os.getenv()`               |
| System Commands  | Run shell commands                       | `os.system()`                             |
| Advanced         | Walk directories                         | `os.walk()`                               |
| Context Usage    | Temporary directory change               | custom `change_directory`                 |
"""

import os
import time

def basic_operations():
    print("Current Working Directory:", os.getcwd())
    print("List of files/folders in cwd:", os.listdir())
    print("User Home Directory:", os.path.expanduser("~"))
    print("OS Name:", os.name)
    print("Environment PATH:", [f"⛔"+i for i in os.environ.get('PATH').split(";")])

def file_and_dir_ops():
    print("\n--- File and Directory Operations ---")
    temp_dir = "demo_dir"
    print(f"❇️ os.path:", os.path)
    temp_file = os.path.join(temp_dir,"sample.txt")

    # Create directory
    os.makedirs(temp_dir, exist_ok=True)

    # Create a file
    # woith === context manager
    # No need to manually call f.close()
    # Safer and cleaner code — avoids file corruption or leaks. __enter__, __exit__
    with open(temp_file, 'w') as f:
        f.write("L1 Hello from os module!\n")
        f.write("L2 Hello from os module!\n")

    # without with
    f = open(temp_file, 'a')
    f.write("line2 Hello from os module \n")
    f.close()

    # Rename file
    new_file = os.path.join(temp_dir, "renamed.txt")
    os.rename(temp_file, new_file)

    # Check existence
    print("File exists:", os.path.exists(new_file))

    # File size
    print("File size:", os.path.getsize(new_file), "bytes")

    # File metadata
    print("Last modified:", time.ctime(os.path.getmtime(new_file)))

    # Cleanup
    os.remove(new_file)
    os.rmdir(temp_dir)

def path_operations():
    print("\n--- Path Operations ---")
    path = "/home/user/docs/file.txt"
    print("Dirname:", os.path.dirname(path))
    print("Basename:", os.path.basename(path))
    print("Split:", os.path.split(path))
    print("Join:", os.path.join("home", "user", "docs", "file.txt"))
    print("Absolute Path .. :", os.path.abspath('..'))
    print("Absolute Path . :", os.path.abspath('.'))

def advanced_operations():
    print("\n--- Advanced Operations ---")
    # Walk through a directory
    for root, dirs, files in os.walk('..'):
        print("Root:", root)
        print("Directories:", dirs)
        print("Files:", files)
        break  # just show the first level

    # Set and get env var
    os.environ['MY_ENV'] = '1234'
    print("Custom Env Var:", os.getenv('MY_ENV'))

    # Execute system command (be cautious)
    print("Running 'echo Hello':")
    os.system('echo Hello')

    # Change directory temporarily
    with change_directory("/tmp"):
        print("Now inside /tmp:", os.getcwd())

# Context manager for safe directory switching
from contextlib import contextmanager

@contextmanager
def change_directory(path):
    original = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original)


# cd C:\Users\Manisha\Documents\GitHub\idea\02-etl-pyspark\src\pyBasicModule\year2025
# python -m module.file_io.os1

if __name__ == "__main__":
    print("os1.py")
    #basic_operations()
    #file_and_dir_ops()
    #path_operations()
    #advanced_operations()
