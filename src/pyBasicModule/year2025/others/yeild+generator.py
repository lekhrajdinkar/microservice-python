"""
- yeild
  - yield returns a value without exiting the function.
  - the function’s state is saved between calls.
  - It produces a generator object.
"""
# ======= Section-1 creator generator (stream-1)
def count_up_to(n):
    i = 1
    while i <= n:
        yield i # pause here, next() will resume
        i += 1

gen = count_up_to(3)
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3
# next(gen) → raises StopIteration

for x in count_up_to(3):
    print(x)  # 1, 2, 3

# ======= Section-2 creator generator (stream-2 file)

def read_lines(file_path):
    with open(file_path) as f: # returns TextIOWrapper
        for line in f:
            yield line.strip()

for line in read_lines("log.txt"):
    print(line)


# ======== Section-3 "yield from"
# Delegating to another generator (sync)
def generator1():
    yield from range(3)
    yield "done"

for val in generator1():
    print(val)
# output: 0 1 2 done

# ============== Section-4 : Async generator (async for)
import asyncio

async def async_count_up_to(n):
    for i in range(n):
        await asyncio.sleep(1)
        yield i

async def main():
    async for num in async_count_up_to(3):
        print(num)

asyncio.run(main())





