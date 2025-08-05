import asyncio

#coroutines
async def task(name, delay):
    print(f"Task {name} started")
    await asyncio.sleep(delay)
    print(f"Task {name} finished")

async def main():
    # 🧩 Running multiple coroutines concurrently
    await asyncio.gather(
        task("A", 2),
        task("B", 1),
    )

asyncio.run(main())

"""
# asyncio.gather(cr1,cr2,etc)
# asyncio.run(cr1)

-- output --
Task A started
Task B started
Task B finished
Task A finished
"""