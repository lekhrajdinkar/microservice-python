from functools import reduce
from itertools import islice

class Stream:
    def __init__(self, iterable):
        self.iterable = iterable

    def map(self, func):
        self.iterable = map(func, self.iterable)
        return self

    def filter(self, func):
        self.iterable = filter(func, self.iterable)
        return self

    def flat_map(self, func):
        def generator():
            for item in self.iterable:
                for sub in func(item):
                    yield sub
        self.iterable = generator()
        return self

    def distinct(self):
        def generator():
            seen = set()
            for item in self.iterable:
                if item not in seen:
                    seen.add(item)
                    yield item
        self.iterable = generator()
        return self

    def sorted(self, key=None, reverse=False):
        self.iterable = iter(sorted(self.iterable, key=key, reverse=reverse))
        return self

    def limit(self, n):
        self.iterable = islice(self.iterable, n)
        return self

    def skip(self, n):
        self.iterable = islice(self.iterable, n, None)
        return self

    def reduce(self, func, initial=None):
        if initial is not None:
            return reduce(func, self.iterable, initial)
        return reduce(func, self.iterable)

    def for_each(self, func):
        for item in self.iterable:
            func(item)

    def to_list(self):
        return list(self.iterable)

    def to_set(self):
        return set(self.iterable)


# Usage:
result = (
    Stream([1, 2, 2, 3, 4, 5, 6])
    .filter(lambda x: x % 2 == 0)
    .map(lambda x: x * x)
    .distinct()
    .limit(2)
    .to_list()
)

print(result)

"""
| Method                 | Description                      |
| ---------------------- | -------------------------------- |
| `map(func)`            | Transform each element           |
| `filter(func)`         | Keep elements matching condition |
| `flat_map(func)`       | Flatten nested iterables         |
| `distinct()`           | Remove duplicates                |
| `sorted(key, reverse)` | Sort elements                    |
| `limit(n)`             | Take first n elements            |
| `skip(n)`              | Skip first n elements            |
| `reduce(func, init)`   | Accumulate values                |
| `for_each(func)`       | Apply function to each item      |
| `to_list()`            | Collect result as list           |
| `to_set()`             | Collect result as set            |

"""
