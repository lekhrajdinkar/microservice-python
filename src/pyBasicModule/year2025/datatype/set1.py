print("🔧 Creating a set")
fruits = {"apple", "banana", "cherry"}
print("Initial Set 🍎🍌🍒:", fruits)

print("\n➕ Adding elements")
fruits.add("orange")
print("After add 🍊:", fruits)

print("\n📌 Updating with multiple items")
fruits.update(["kiwi", "grape"])
print("After update 🥝🍇:", fruits)

print("\n❌ Removing elements")
fruits.remove("banana")  # ❌ throws error if not found
fruits.discard("pear")   # ✅ no error if not found
print("After remove 🍌 and discard 🍐:", fruits)

print("\n🚪 Popping random item")
item = fruits.pop()
print("Popped:", item)
print("Remaining Set:", fruits)

print("\n🔁 Set operations")
tropical = {"mango", "pineapple", "kiwi"}
print("Tropical Set:", tropical)

print("📍 Union:", fruits.union(tropical))
print("🔁 Intersection:", fruits & tropical)
print("➖ Difference (fruits - tropical):", fruits - tropical)
print("🔄 Symmetric Difference:", fruits ^ tropical)

print("\n🧹 Clearing set")
fruits.clear()
print("After clear:", fruits)
