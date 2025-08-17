-  **package** is a directory containing an `__init__.py`
- object creation : `__new__(T,V) + __init__`
- **enum.Enum**
- **classes**
    -  constructor: `def __init__(self):`
    - no getters/setters, can access attributes directly
    - weak : private/protected/public : __ , _ ,  --> not enforced, Name mangling only
    - **instance variable** with self.xxxx
    - **static variable** -> var without self + `@staticmethod`
    - `@classmethod`
        - def my_class_method(cls, arg1, arg2):
        - First parameter is **cls**, representing the class itself, like self represents the instance.
        - MyClass.my_class_method() or obj.my_class_method()
    - create object without **new operator**, unlike java
    - `obj.__class__` -> Reference to class
- **Abstraction** : abstract class using **abc module**
    - no native interface
    - module:ABC + @abstractmethod
- **Polymorphism**
    - only **overriding** happens, since duck typing.
    - **overloading**  (no native support)
        - achieve same with *args, **kwargs ( to dict)
        - with `@singledispatch` [02_oops.py | section-2](../../src/pyBasicModule/year2025/style_oops/02_oops.py)
        - fact: last defined method with the same name overrides previous ones
- **error handling**:
    - try, except MyError as e, finally



