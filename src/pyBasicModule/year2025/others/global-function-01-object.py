class Person:
    def __init__(self):
        self.name = "Alice"
        self.age = 30

p = Person()

# hasattr() - check if attribute exists
print(hasattr(p, 'name'))    # True
print(hasattr(p, 'email'))   # False

# getattr() - get attribute value
print(getattr(p, 'age'))     # 30

# setattr() - set attribute value
setattr(p, 'name', 'Bob')
print(p.name)                # Bob

# setattr() - create new attribute
setattr(p, 'email', 'bob@example.com')
print(p.email)               # bob@example.com

# delattr() - delete attribute
delattr(p, 'age')
print(hasattr(p, 'age'))     # False
