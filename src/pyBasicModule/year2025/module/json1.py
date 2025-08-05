"""
| Feature                 | Function         | Example                           |
| ----------------------- | ---------------- | --------------------------------- |
| Serialize to string     | `json.dumps()`   | `json.dumps(obj)`                 |
| Deserialize from string | `json.loads()`   | `json.loads(json_str)`            |
| Write to file           | `json.dump()`    | `json.dump(obj, file)`            |
| Read from file          | `json.load()`    | `json.load(file)`                 |
| Pretty print            | `indent=4`       | `json.dumps(obj, indent=4)`       |
| Sort keys               | `sort_keys=True` | `json.dumps(obj, sort_keys=True)` |
| Handle custom objects   | `default=`       | `json.dumps(obj, default=...)`    |

"""

import json
from pathlib import Path


def basic_json_usage():
    print("\n🧩 Basic JSON Operations")

    data: dict = {
        "name": "Lekhraj",
        "age": 33,
        "skills": ["Python", "AWS", "Docker"],
        "active": True
    }
    # Serialize Python object/dict to JSON string
    json_str = json.dumps(data)
    print("📤 JSON String:", json_str, type(json_str), type(data))

    # Deserialize JSON string to Python object
    parsed: dict = json.loads(json_str)
    print("📥 Parsed Python Object:", parsed['name'], type(parsed))

def write_read_json_file():
    print("\n📂 File Read/Write with JSON")

    data = {
        "project": "Pathfinder",
        "version": 1.2,
        "features": ["login", "dashboard", "analytics"]
    }

    path = Path("sample.json")
    print(type(data))
    # Write JSON to file
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    print("💾 JSON written to file")

    # Read JSON from file
    with open(path, 'r') as f:
        content = json.load(f)
    print("📖 Read from file:", content, type(content))

    # Cleanup
    path.unlink()

def pretty_and_sorted():
    print("\n🎨 Pretty Print and Sort Keys")

    obj = {
        "z": 1,
        "a": 2,
        "m": 3
    }

    # Pretty print with sorted keys
    pretty = json.dumps(obj, indent=2, sort_keys=True)
    print("🔠 Sorted and Pretty:\n", pretty)

def advanced_usage():
    print("\n🧠 Advanced JSON Usage")

    class User:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    def user_encoder(obj):
        if isinstance(obj, User):
            return {"name": obj.name, "age": obj.age}
        raise TypeError("❌ Not serializable")

    user = User("Dinkar", 30)

    # Serialize custom object
    encoded = json.dumps(user, default=user_encoder)
    print("👨‍💻 Custom Object Serialized:", encoded)

    # Deserialize manually
    decoded = json.loads(encoded)
    print("📥 Custom Object Deserialized:", decoded)

if __name__ == "__main__":
    basic_json_usage()
    write_read_json_file()
    #pretty_and_sorted()
    #advanced_usage()
