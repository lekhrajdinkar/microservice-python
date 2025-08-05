# python -m src.pyBasicModule.year2025.others.global-function-02-type-conversion.py 🏃‍♂️

# ========= Section-1 : Type Conversion
def typeConverion():
    x = "123"
    y = int(x)          # string to int
    z = float(y)        # int to float
    s = str(z)          # float to string
    b = bool(s)         # non-empty string to True

    print(y, type(y))   # 123 <class 'int'>
    print(z, type(z))   # 123.0 <class 'float'>
    print(s, type(s))   # '123.0' <class 'str'>
    print(b, type(b))   # True <class 'bool'>

    # List & Set
    t = (1, 2, 3)
    l = list(t)         # tuple to list
    s = set(l)          # list to set

    print(l, type(l))   # [1, 2, 3] <class 'list'>
    print(s, type(s))   # {1, 2, 3} <class 'set'>

    # Type Checking - isinstance(T,obj1) / type(obj1) == "T"
    print(isinstance(l, list))   # True
    print(isinstance(s, dict))   # False
    print(type(10) == int)       # True

#=============== Section-2 : More on int (), multiple variant
def typeConverion_int_more():
    print(int("123"))          # 123 (from string)
    print(int("FF", 16))       # 255 (hex string)
    print(int(4.99))           # 4 (from float)
    print(int(True))           # 1 (from bool)
    print(int(b"100"))         # 100 (from bytes)

if (__name__ == "__main__"):
    typeConverion();
    typeConverion_int_more();