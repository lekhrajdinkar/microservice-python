# Randon Topic
## kwarg | arg
- `*args` → captures extra positional arguments as a **tuple**
- `**kwargs` → captures extra keyword arguments as a **dict**

---
## __ name __
- `__name__`: special built-in variable in every Python file (`module-1`.py)
  - `__main__`: if module ran directly
  - `module-1` : if module ran by being imported

---
## Generator
**generator** 
- is a function containing `yield`
- produces a sequence of values over time using yield keyword
- one value at a time, return and pause
- All generators are **iterators**, not vice versa. both Returns New Collections 👈

Use Case
- want to stream data (e.g. files, DB rows)
- work with large/infinite datasets
- **need lazy evaluation.**

```python
def f1():
    yield 10
    yield 20
    yield 30
```

```blueprint
f1() ──→ generator
          │
          ├─ next() → 10
          ├─ next() → 20
          ├─ next() → 30
          └─ next() → StopIteration

or, loop over generator
```
---
`yield` keyword
- yield returns a value without exiting the function.
- the function’s run state is saved between calls.
- It produces a **generator** object.
> **yield** helps a function stream multiple return values one at a time, instead of returning them all at once.

|         | **return** ,   vs         | **yield**  (stream)           |
| -------------- |---------------------------|-------------------------------|
| Ends function? | Yes                       | No (pauses and resumes)       |
| Use case       | One result only           | Sequence of results over time |
| Memory         | Stores all values at once | Streams one value at a time   |

@[code:7-22](../../../src/pyBasicModule/year2025/others/yeild-and-generator.py)

---
`yield from`  
- Delegating to another generator (sync)

```python
def inner():
    yield 1
    yield 2
    yield 3

# With yield from:
def outer():
    yield from inner()
    
# Without yield from:
def outer():
    for x in inner():
        yield x
```
@[code:33-42](../../../src/pyBasicModule/year2025/others/yeild-and-generator.py)


---
`async for` for "Async generator"
@[code:44-56](../../../src/pyBasicModule/year2025/others/yeild-and-generator.py)

---
## Generator Expression ⭐
- like a **list comprehension**, but produces items one at a time, **using lazy evaluation**
- saves memory, consume less, and is faster for large data
- syntax: **(expression for item in iterable if condition)**
- eg: 
  - `(x*x for x in range(5))`
  - `(x*x for x in range(10) if x % 2 == 0)`

---
## Comprehension ⭐
> Syntax: 
> - Comprehension :        [x] , {x}, {x:v}, 
> - Generator Expression : (x)

- concise ways to create **new** collections like lists, sets, or dictionaries
- **Eager Evaluation**: Evaluates all items immediately.
- Stores all values in memory as a full list.
- example 
  - `even_set_squares = [x*x for x in range(10) if x % 2 == 0] ` **List** comprehension
  - `even_set = {x for x in range(10) if x % 2 == 0}`  **set** comprehension
  - `squares = {x: x * x for x in range(5)}`   **dict** comprehension

| Feature                  | Java Stream API                     | Python Equivalent                          |
| ------------------------ | ----------------------------------- | ------------------------------------------ |
| **Filtering**            | `.filter(x -> x > 0)`               | `[x for x in list if x > 0]`               |
| **Mapping/Transforming** | `.map(x -> x * 2)`                  | `[x * 2 for x in list]`                    |
| **Collect to List**      | `.collect(Collectors.toList())`     | Result is already a list                   |
| **Lazy evaluation**      | Intermediate ops are lazy           | Use generator expressions (`(x for x...)`) |
| **Parallel processing**  | `.parallelStream()`                 | Use multiprocessing/threading manually     |
| **Chaining operations**  | `stream().filter().map().collect()` | Use nested comprehensions or `map/filter`  |

@[code:1-10](../../../src/pyBasicModule/year2025/datatype/list_and_iterable1.py)

---
## collection
- generator, Iteration/Streams vs Comprehensions
- negative and nested indexing
- can omit () in tuple
- when to use, which datatype
- str1.isnumeric()
- [::] is hardcoded vs **slice**(start,end,step) is  dynamic ⬅️
- **global build in** - iterable
- l = map(func, iterable)
- l = filter(func, iterable) – Filter items matching condition
- sum | all | any([...]) --> for numeric
- custom class (wrapped list) with __iter__() and __next__() for iterable objects : [dunder1.py](../../../src/pyBasicModule/year2025/others/dunder1.py)
- **shelve** [shelve1.py](../../../src/pyBasicModule/year2021/modules/shelve1.py) === like dict [str|any] ⬅️
- [1,2,3] * 2
- [0] * 2
- [[0] * 2] * 2    #2d Array
- for a,b in **zip**(arr1,arr2) ⬅️
- priority-Queue : heapq ⬅️

---
## decorator ❓
- decorator
- Mutability or performance comparison

---
##  deepcopy
- [copy1.py](../../../src/pyBasicModule/year2025/others/copy1.py)
- time --> time.struct_time --> named tuple

---
## memory mgt
- automatic and built-in,
- reference count goes to 0, obj deleted
- private heap for all object allocations.
- Use `del, gc.collect()` for manual cleanup if needed.
- __del__() === destroy in java
- **pymalloc** manages small objects in arenas : int 1to 256, string === **interning**
- cyclic garbage collector for a → b → a
- GC runs periodically to collect unused cyclic references

| 🔧 Tool/Module    | 🧠 Purpose                            |
| ----------------- | ------------------------------------- |
| `sys.getsizeof()` | Size in bytes of an object            |
| `gc` module       | Control garbage collector             |
| `tracemalloc`     | Track memory allocations              |
| `objgraph`        | Visualize memory object relationships |

| Intent         | Python | Java        |
| -------------- | ------ | ----------- |
| Check value    | `==`   | `.equals()` |
| Check identity | `is`   | `==`        |

---
## Threads
- **GIL** global interpreter lock
- import threading + [thread1.py](../../../src/pyBasicModule/year2025/others/thread1.py)

---
## Async
- library : asyncio (has **eventloop**)
- async with - `( __aenter__() , __aexit__() )` ⬅️
- with - `( __enter__() , __exit__() )`

| Feature          | `with`                  | `async with`                      |
| ---------------- | ----------------------- | --------------------------------- |
| Type             | Synchronous             | Asynchronous                      |
| Used with        | Files, locks, etc.      | Async resources (e.g., HTTP, DB)  |
| Requires `await` | ❌ No                    | ✅ Yes (must be in an `async def`) |
| Under the hood   | `__enter__`, `__exit__` | `__aenter__`, `__aexit__`         |

- `async` and `await` === same like in JS
- Python’s keywords for asynchronous programming,
- enabling you to write code that runs concurrently without blocking.
- basically, Avoid blocking the main thread.
- `async def abc():` defines a **coroutine function** + return **coroutine objects**, not direct results.
- `result = await abc()` :
- await pauses the coroutine, until the awaited task completes, allowing other tasks to run in the meantime.
- Once finished, await extracts the actual returned value from that coroutine object.
- await "unwraps" the coroutine object into its direct result.
- purpose : To handle I/O-bound operations efficiently (e.g., network calls, file I/O).

| Keyword         | Purpose                                           |
| --------------- | ------------------------------------------------- |
| `async def`     | Defines a coroutine function                      |
| `await`         | Waits for a coroutine or awaitable (non-blocking) |
| `asyncio.run()` | Runs the event loop and the main coroutine        |

- vs Js

| Feature                | Python (`async`/`await`)                                | JavaScript (`Promise` + `async`/`await`)             |
| ---------------------- | ------------------------------------------------------- | ---------------------------------------------------- |
| Async function returns | Coroutine object                                        | Promise                                              |
| `await`                | Waits for coroutine to complete, returns resolved value | Waits for Promise to resolve, returns resolved value |
| Event loop             | `asyncio` event loop manages coroutines                 | JavaScript event loop manages promises               |
| Syntax                 | `async def func(): ... await ...`                       | `async function func() { await ... }`                |

- **Eventloop** ⬅️
- It lets Python run many tasks "at once" **without using threads**,
- by running bits of one task, then another, and so on.

```
🔁 The event loop:
Picks up one coroutine.
Runs it until it hits an await (e.g., I/O or sleep).
Switches to another coroutine that’s ready to run.
Repeats until all tasks are done.
```

| Function                 | Description                              |
| ------------------------ | ---------------------------------------- |
| `asyncio.run(coro)`      | Starts event loop and runs coroutine     |
| `asyncio.create_task()`  | Schedules a coroutine to run in parallel |
| `await asyncio.sleep(n)` | Non-blocking delay                       |
| `asyncio.gather()`       | Run multiple coroutines concurrently     |

---
## functional

| Type                          | Description          | Example         |
| ----------------------------- | -------------------- | --------------- |
| `function`                    | Function object      | `def f(): pass` |
| `lambda`                      | Anonymous function   | `lambda x: x*2` |
| `generator`                   | Lazy sequence        | `yield`         |
| `coroutine`                   | For async/await      | `async def`     |
| `classmethod`, `staticmethod` | Class/static methods |                 |

- filter, map, any, all, sum

---
## Exception
- traceback