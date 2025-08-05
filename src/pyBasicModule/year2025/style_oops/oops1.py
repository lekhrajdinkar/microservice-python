# =================== section-1 : abstraction

from abc import ABC, abstractmethod

class Animal(ABC):
    count = 0  # static field
    @abstractmethod
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self): # Method Overriding
        print("Woof")

# =================== section-2 : overloading

from functools import singledispatchmethod

class Printer:
    @singledispatchmethod
    def print_data(self, data):
        print("Unsupported type")

    @print_data.register
    def _(self, data: int):
        print("Integer:", data)

    @print_data.register
    def _(self, data: str):
        print("String:", data)

    @print_data.register
    def _(self, data: list):
        print("List:", data)

p = Printer()
p.print_data(42)          # Integer: 42
p.print_data("hello")     # String: hello
p.print_data([1, 2, 3])   # List: [1, 2, 3]

# =================== section-3 : Enum
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# Accessing values
print(Color.RED)           # Color.RED
print(Color.RED.name)      # RED
print(Color.RED.value)     # 1

for color in Color:
    print(color.name, color.value)

# Using Enum in Condition
def get_color_code(color):
    if color == Color.RED:
        return "#FF0000"
    elif color == Color.GREEN:
        return "#00FF00"
    elif color == Color.BLUE:
        return "#0000FF"

print(get_color_code(Color.GREEN))  # #00FF00

# Enum with Custom Methods
class Status(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"

    def is_complete(self):
        return self == Status.DONE

print(Status.DONE.is_complete())  # True

# Enum with auto() (automatically assign values)
from enum import Enum, auto

class Priority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

print(list(Priority))
# [<Priority.LOW: 1>, <Priority.MEDIUM: 2>, <Priority.HIGH: 3>]

# =================== section-4 : *args **kwargs

def add_numbers(*args):
    print(args)
    return sum(args)
add_numbers(1, 2, 3)  # (1, 2, 3) → 6

def print_details(**kwargs):
    print(kwargs)
print_details(name="Alice", age=30) # {'name': 'Alice', 'age': 30}

# Combine *args and **kwargs
def demo(a, *args, **kwargs):
    print("a:", a)
    print("args:", args)
    print("kwargs:", kwargs)
demo(1, 2, 3, x=10, y=20)
tuple1= (2, 3);   dict1 = { "x": 10, "y":20 };
demo(1, tuple1, dict1);
# a: 1
# args: (2, 3)
# kwargs: {'x': 10, 'y': 20}




