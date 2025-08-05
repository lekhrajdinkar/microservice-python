"""
🪞 Shallow Copy (copy.copy())
Copies the outer object, but inner nested objects are still shared (referenced).
✅ Fast, but ⚠️ can cause bugs when inner items are mutated.
"""

import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)

shallow[0][0] = 99
print(original)  # [[99, 2], [3, 4]] 😬

"""
Deep Copy (copy.deepcopy())
Recursively copies all levels of the object (fully independent clone).
✅ Safe for complex/nested structures.
"""

import copy

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

deep[0][0] = 99
print(original)  # [[1, 2], [3, 4]] ✅


"""
| Feature          | Shallow Copy             | Deep Copy                      |
| ---------------- | ------------------------ | ------------------------------ |
| 📦 Module        | `copy.copy()`            | `copy.deepcopy()`              |
| 🔁 Outer Object  | New object               | New object                     |
| 🔁 Inner Objects | Shared (same references) | Cloned (recursively)           |
| 💡 Use Case      | Flat/non-nested objects  | Nested/mutable complex objects |
| 🧠 Performance   | Faster                   | Slower                         |

"""
