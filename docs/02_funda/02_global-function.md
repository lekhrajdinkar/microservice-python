- fact: ⬅️
    - `int("42")` === `int.__new__(int, "42")` // int is class (right side one)
    - int() is a built-in function,
    -  It internally calls the constructor of the int class.

---  
## 1. Type Conversion & Type Checking
| Function       | Purpose                   |
| -------------- | ------------------------- |
| `int()`        | Convert to integer        |
| `float()`      | Convert to float          |
| `str()`        | Convert to string         |
| `bool()`       | Convert to boolean        |
| `complex()`    | Complex number            |
| `list()`       | Convert to list           |
| `tuple()`      | Convert to tuple          |
| `set()`        | Convert to set            |
| `frozenset()`  | Immutable set             |
| `dict()`       | Convert to dict           |
| `bytes()`      | Immutable byte sequence   |
| `bytearray()`  | Mutable byte sequence     |
| `memoryview()` | View of bytes             |
| `chr()`        | Unicode code to character |
| `ord()`        | Character to Unicode code |
| `bin()`        | Binary string             |
| `hex()`        | Hexadecimal string        |
| `oct()`        | Octal string              |
| `type()`       | Get type                  |
| `isinstance()` | Check instance            |
| `issubclass()` | Check subclass            |

## 2. Iterables, Iterators & Functional Programming
| Function      | Purpose                     |
| ------------- | --------------------------- |
| `range()`     | Sequence of numbers         |
| `enumerate()` | Index + value               |
| `zip()`       | Combine iterables           |
| `map()`       | Apply function to each item |
| `filter()`    | Filter by condition         |
| `iter()`      | Get iterator                |
| `next()`      | Next item from iterator     |
| `reversed()`  | Reverse iterator            |
| `sorted()`    | Return sorted list          |
| `slice()`     | Slice object                |
| `sum()`       | Sum values                  |
| `all()`       | True if all true            |
| `any()`       | True if any true            |
| `max()`       | Maximum value               |
| `min()`       | Minimum value               |

## 3. Object/Attribute Handling
| Function     | Purpose                    |
| ------------ | -------------------------- |
| `getattr()`  | Get attribute              |
| `setattr()`  | Set attribute              |
| `delattr()`  | Delete attribute           |
| `hasattr()`  | Check attribute            |
| `vars()`     | Object’s `__dict__`        |
| `dir()`      | List names in scope/object |
| `globals()`  | Global symbol table        |
| `locals()`   | Local symbol table         |
| `callable()` | Is callable                |
| `id()`       | Identity of object         |
| `hash()`     | Hash value                 |
| `object()`   | Base object                |

## 4. Evaluation & Execution
| Function       | Purpose                       |
| -------------- | ----------------------------- |
| `eval()`       | Evaluate string as expression |
| `exec()`       | Execute Python code           |
| `compile()`    | Compile code string           |
| `__import__()` | Dynamic import                |

## 5. Classes & Methods
| Function         | Purpose              |
| ---------------- | -------------------- |
| `classmethod()`  | Define class method  |
| `staticmethod()` | Define static method |
| `property()`     | Define property      |
| `super()`        | Access superclass    |

## 6. Input/Output
| Function       | Purpose                   |
| -------------- | ------------------------- |
| `help()`       | Show help                 |
| `repr()`       | Developer-readable string |
| `ascii()`      | Escape non-ASCII          |
| `breakpoint()` | Trigger debugger          |


## 7. Debugging & Introspection
| Function   | Purpose                |
| ---------- | ---------------------- |
| `abs()`    | Absolute value         |
| `round()`  | Round float            |
| `pow()`    | Power/exponentiation   |
| `divmod()` | Quotient and remainder |
| `format()` | Format string          |
