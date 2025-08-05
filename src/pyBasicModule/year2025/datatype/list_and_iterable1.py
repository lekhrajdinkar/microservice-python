# ==========================
# All Operations
# =========================

def listDemo():
    # 📄 Create a list
    fruits = ["apple", "banana", "cherry"]

    # 🔍 Access items
    print(fruits[0])        # apple
    print(fruits[-1])       # cherry
    print(fruits[1:])       # ['banana', 'cherry']

    # ✍️ Update an item
    fruits[1] = "blueberry"

    # ➕ Add items
    fruits.append("date")               # Add to end
    fruits.insert(1, "kiwi")            # Insert at index

    # ➖ Remove items
    fruits.remove("apple")              # Remove by value
    last = fruits.pop()                 # Remove last item
    del fruits[0]                       # Delete by index

    # 🔁 Loop over list
    for fruit in fruits:
        print(fruit)

    # 📦 Combine lists
    more_fruits = ["mango", "pear"]
    fruits += more_fruits               # Extend list

    # 🧹 Clear list
    # fruits.clear()

    # ✅ Check existence
    if "mango" in fruits:
        print("Mango is here!")

    # 🔄 Sort and reverse
    fruits.sort()
    fruits.reverse()

    # 🧾 Length and copy
    print(len(fruits))                 # Number of items
    copy_list = fruits.copy()

    # 🔁 List comprehension
    lengths = [len(f) for f in fruits]

    # 🧾 Final output
    print("Final fruits:", fruits)
    print("Lengths:", lengths)

    # ============= Section-2 : zip

    names = ["Alice", "Bob"]
    ages = [25, 30]
    for name, age in zip(names, ages):
        print(name, age)

    # ============= Section-3 :  enumerate

    items = ['a', 'b', 'c']
    for index, value in enumerate(items):
        print(index, value)

    # ============= Section-4 :  itertools — Powerful Looping Utilities

    from itertools import product
    for x in product([1, 2], ['a', 'b']):
        print(x)
    # (1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')

    # ======== Section -5  Loop tips

    ## 1 Use Built-in Functions Instead of Manual Loops
    my_list = [1,2,3,4,5,6]
    # ✅ Fast
    total = sum(my_list)

    # ❌ Slower
    total = 0
    for x in my_list:
        total += x

    ## 2 Use List Comprehensions Instead of for Loops
    # ✅ Fast
    squares = [x * x for x in range(1000)]

    # ❌ Slower
    squares = []
    for x in range(1000):
        squares.append(x * x)

    ## 3 Avoid Repeated Computation in Loop
    # ✅ Good
    length = len(my_list)
    for i in range(length):
        pass

    # ❌ Bad
    for i in range(len(my_list)):
        pass

    ## 4 Use enumerate() and zip() Instead of Manual Indexing

    ## 5 Saves memory by not storing the full list in RAM
    # ✅ Better for big data
    total = sum(x * x for x in range(1000000)) # Generator expression
    # ❌ List comprehension stores all
    total = sum([x * x for x in range(1000000)])


def comprehension_demo():
    squrare = [x*x for x in range(10) if x % 2 == 0]
    # List comprehension : fast + consume memory
    # <class 'list'>
    print(f"comprehension :: [x*x for x in range(10) if x % 2 == 0]", squrare, type(squrare))

    print("✅ Dictionary Comprehension : Create a lookup dictionary for word lengths")
    words = ["apple", "banana", "cherry"]; print(f" 🟢 source :: ",words);
    word_lengths = {word: len(word) for word in words}
    print("target :: ",word_lengths)  # {'apple': 5, 'banana': 6, 'cherry': 6}

    print("🔸 Filter out items with zero quantity:")
    inventory = {"apples": 10, "oranges": 0, "bananas": 5}; print(f" 🟢 source :: ", inventory)
    available = {item: qty for item, qty in inventory.items() if qty > 0}
    print("target :: ",available)  # {'apples': 10, 'bananas': 5}

    print("🔸 Extract  names from email addresses")
    emails = ["user1@gmail.com", "admin@yahoo.com", "test@outlook.com"]; print(f" 🟢 source :: ", emails)
    domains = [email.split("@")[0] for email in emails]
    print("target :: ",domains)  # ['gmail.com', 'yahoo.com', 'outlook.com']

    print("✅ Set Comprehension: Remove duplicates  + lowercase")
    words = ["Apple", "apple", "Banana", "BANANA"]; print(f" 🟢 source :: ", emails)
    unique_words = {word.lower() for word in words}
    print("target :: ",unique_words)  # {'apple', 'banana'}

    matrix = [[1, 2], [3, 4], [5, 6]]; print(f" 🟢 source :: ", matrix)
    flat = [num for row in matrix for num in row]
    print("target :: ",flat)  # [1, 2, 3, 4, 5, 6]

#==================
# GENERATOR
#==================
def generation_demo():
    #<generator object generation_demo.<locals>.<genexpr> at 0x0000022B6A09C450> <class 'generator'>
    print("✅ Generator Comprehension")
    square_gen = (x * x for x in range(10) if x % 2 == 0)  # Generator expression
    print("generator :: (x*x for x in range(10) if x % 2 == 0)", square_gen, type(square_gen))
    for item in square_gen:
        print(item, type(item), f"ℹ️")

from typing import Generator
import os
def read_file_by_line_generator_1(filename: str = "datatype/bigfile.txt") -> Generator[str, None, None]:
    print(os.getcwd())
    try:
        with open(filename, "r") as file:
            for line in file:
                stripped = line.strip()
                if stripped:  # Skip blank lines
                    yield stripped
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

def read_file_by_line_generator_2(filename: str ) -> Generator[str, None, None]:
    return (line for line in open(filename, "r"))

def list_prg_1_indexinfWithRange():
    list2 = ["item1","item2","item3","item4","item5"]
    item_to_find = 'item4'
    for index in range(0,len(list2)):
        if list2[index] == item_to_find:
            print(list2[index], ' found !!')
            break
        else:
            print(list2[index], ' unmatched')

"""
| Type                     | Returns New Collection? | Original Mutated? |
| ------------------------ | ----------------------- | ----------------- |
| **List comprehension**   | ✅ Yes                   | ❌ No              |
| **Dict comprehension**   | ✅ Yes                   | ❌ No              |
| **Set comprehension**    | ✅ Yes                   | ❌ No              |
| **Generator expression** | ✅ Lazy generator        | ❌ No              |

"""

# =============== Python Built-ins  =======


def global_built_in():
    import objgraph

    # iter() :: manually iterating over a collection. ⬅️
    nums = [10, 20, 30]
    it = iter(nums)
    print(next(it))  # 10
    print(next(it))  # 20

    print(sum([1, 2, 3], 10))  # 16 sum()

    # ✅ all() – True if all elements are True
    print(all([True, 1, "ok"]))       # True
    print(all([True, 0, "ok"]))       # False

    # ⚠️ any() – True if any
    print(any([False, 0, "", "Hi"]))  # True
    print(any([False, 0, ""]))        # False

    # newSequence = map( lambda , iterable)
    print(map(lambda x:x>20, nums))

    # https://graphviz.org/download + set path : bin
    print("🔍 Most common types:")
    objgraph.show_most_common_types(limit=5)
    print("\n Show backref graph of 'a'")
    objgraph.show_backrefs([nums], filename='backrefs.png')

if __name__ == '__main__':
    global_built_in()


