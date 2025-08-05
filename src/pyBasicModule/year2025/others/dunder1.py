def filter1(x):
    return x

class MyList:
    def __init__(self, items):
        self.data = list(items)  # store as a list internally
        self.username = "harcoded-userName"
        self.email = "harcoded-userName@gmail.com"

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __delitem__(self, index):
        del self.data[index]

    def __iter__(self):
        return iter(self.data)
    #def __next__(self): pass

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data

    def __add__(self, other):
        return MyList(self.data + other.data)

    def __eq__(self, other):
        return

    def __repr__(self):
        return f"MyList({self.data})"

    def __bool__(self):
        return bool(self.items)  # True if list is not empty

    def __hash__(self):
        return hash((self.username, self.email))

    def __eq__(self, other):
        if not isinstance(other, MyList):
                return NotImplemented  ## NotImplemented
        return self.data == other.data


a = MyList([1, 2, 3])
b = MyList([4, 5])
c = MyList([])

print(a[1])           # __getitem__ → 2
a[1] = 20             # __setitem__
print(a)              # __repr__ → MyList([1, 20, 3])

del a[0]              # __delitem__
print(a)              # MyList([20, 3])

for x in a:           # __iter__
    print(x)          # prints 20 and 3

print(len(a))         # __len__ → 2
print(3 in a)         # __contains__ → True

c = a + b             # __add__
print(c)              # MyList([20, 3, 4, 5])

print(c == MyList([20, 3, 4, 5]))  # __eq__ → True

if a:
    print("object-a is not empty")   # ✅ This prints

if c:
    print("object-a is not empty")   # ❌ This doesn't print

print(hash(a))