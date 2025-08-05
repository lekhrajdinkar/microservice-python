str = """
✅ Basic Syntax
"{}".format(value)
"{0}".format(value1)
"{name}".format(name=value2)

always returns a string, convert str to desired type ⬅️

=================================================

🔢 Integer Formatting
| Format                   | Output            |
| ------------------------ | ----------------- |
| `"{}".format(42)`        | `'42'`            |
| `"{:05}".format(42)`     | `'00042'`         |
| `"{:<5}".format(42)`     | `'42   '`         |
| `"{:>5}".format(42)`     | `'   42'`         |
| `"{:^5}".format(42)`     | `' 42  '`         |
| `"{:b}".format(10)`      | `'1010'` (binary) |
| `"{:x}".format(255)`     | `'ff'` (hex)      |
| `"{:,}".format(1000000)` | `'1,000,000'`     |

🌊 Float Formatting
| Format                     | Output           |
| -------------------------- | ---------------- |
| `"{:.2f}".format(3.14159)` | `'3.14'`         |
| `"{:10.2f}".format(3.14)`  | `'      3.14'`   |
| `"{:<10.2f}".format(3.14)` | `'3.14      '`   |
| `"{:+.2f}".format(3.14)`   | `'+3.14'`        |
| `"{:.0f}".format(3.99)`    | `'4'`            |
| `"{:.2%}".format(0.123)`   | `'12.30%'`       |
| `"{:e}".format(1234567)`   | `'1.234567e+06'` |

🔤 String Formatting
| Format                     | Output         |
| -------------------------- | -------------- |
| `"{}".format("abc")`       | `'abc'`        |
| `"{:>10}".format("abc")`   | `'       abc'` |
| `"{:<10}".format("abc")`   | `'abc       '` |
| `"{:^10}".format("abc")`   | `'   abc    '` |
| `"{:.2}".format("abcdef")` | `'ab'`         |
"""

def formatingDemo1():
    # 📚 List Formatting (via unpacking)
    lst = [1, 2, 3]
    print("List: {}, {}, {}".format(*lst))  # List: 1, 2, 3
    print("List2: {}, {}, {}".format(11,2,3,55))

    print("JOINING :: ", ", ".join("Item {}".format(x) for x in lst))  # Item 1, Item 2, Item 3

    # 🔁 Numbered & Named Placeholders
    print("{0} + {1} = {2}".format(2, 33, 5))  # 2 + 3 = 5
    print("{name} is {age} years old".format(name="Bob", age=25))

    # 🗂️ Dict Formatting
    person = {"name": "Alice", "age": 30}
    print("Name: {name}, Age: {age}".format(**person))  # Name: Alice, Age: 30

    #print(str)

def p(*args):
    for item in args:
        print("{:>50}".format(item))

