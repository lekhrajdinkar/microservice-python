def outer():
    x = 5

    def inner():
        nonlocal x
        x = 10  # modifies x in outer()

    print("Before inner:", x)
    inner()
    print("After inner:", x)

outer()

# Before inner: 5
# After inner: 10

# =====================


x = 5

def foo():
    global x
    x = 10  # Modifies the global variable 'x'
    print("Inside foo:", x)

foo()             # Inside foo: 10
print("Outside:", x)  # Outside: 10 (global x modified)


"""
| Keyword    | Scope Modified                   | Usage Context                     |
| ---------- | -------------------------------- | --------------------------------- |
| `global`   | Module-level global variables    | Modify globals inside functions   |
| `nonlocal` | Nearest enclosing function scope | Modify outer function’s variables |

"""