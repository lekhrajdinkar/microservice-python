"""
... is a built-in constant called Ellipsis.
It’s of type: EllipsisType


| Usage Area          | Purpose                              |
| ------------------- | ------------------------------------ |
| Function/Class body | Placeholder (like `pass`)            |
| NumPy               | Multi-dimensional slicing shortcut   |
| Custom logic        | Used as a sentinel or special marker |

"""

# 1. 🧱 Placeholder in functions or classes
def my_func():
    return ...

result = my_func()
print(result)
print(type(result))

# Ellipsis
# <class 'ellipsis'>

class MyClass:
    def method(self):
        ...
