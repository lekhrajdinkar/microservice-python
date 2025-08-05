def dictDemo():
    # Create a dictionary
    person = {
        "name": "Alice",
        "age": 30,
        "city": "New York"
    }

    # 🔍 Accessing values
    print(f"🔍",person["name"])            # Alice
    print(f"🔍",person.get("age"))         # 30
    print(f"🔍 get default : ",person.get("gender", "N/A"))  # Default if key doesn't exist

    # ✍️ Updating values
    person["age"] = 31

    # ➕ Adding new key-value pair
    person["job"] = "Engineer"

    # ❌ Deleting a key
    del person["city"]
    person.pop("job")

    # ✅ Check if key exists
    if "name" in person:
        print(f"✅","Name exists")

    # 🔁 Loop through keys and values
    for key, value in person.items():
        print(f"🔁 {key}: {value}")

    # 🔑 Get only keys or values
    print(f"🔑 keys",list(person.keys()))    # ['name', 'age']
    print(f"🔑 values",list(person.values()))  # ['Alice', 31]

    # 📦 Copy dictionary
    person_copy = person.copy()

    # 🔁 Merge dictionaries (Python 3.9+)
    extra = {"country": "USA"}
    person |= extra  # same as person.update(extra)

    # 🧹 Clear all entries
    # person.clear()

    # 🧾 Final result
    print("Final:", person)

def dict_comp_demo():
    squares = {x: x * x for x in range(5)}
    print("🟩 Squares:", squares)

    original = {'a': 1, 'b': 2, 'c': 3}
    inverted = {v: k for k, v in original.items()}
    print("🔁 Inverted:", inverted)

    filtered = {k: v for k, v in original.items() if v > 1}
    print("🔎 Filtered:", filtered)


if __name__ == '__main__':
    dictDemo()
    dict_comp_demo()