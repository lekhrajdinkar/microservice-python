import requests

def client1():
    url = "http://localhost:8000/upload"
    files = {
        "file": ("example.txt", open("example.txt", "rb")),
    }
    data = {
        "description": "Sample file upload via FastAPI"
    }

    response = requests.post(url, files=files, data=data)
    print(response.json())

def client2():
    """
    Sets Content-Type: multipart/form-data automatically.
    Sends a file and a text field (description) in the same request.
    """
    url = "http://localhost:8000/upload"
    files = {
        'file': ('example.txt', open('example.txt', 'rb')),
        'description': (None, 'Sample file upload')
    }

    response = requests.post(url, files=files)
    print(response.status_code)

def client3_download():
    url = "http://localhost:8000/download"
    response = requests.get(url)

    with open("local_copy.txt", "wb") as f:
        f.write(response.content)

    print("Downloaded!")

# ------- ASYNC Client ------

import aiohttp
import asyncio

async def fetch1():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/download") as response:
            data = await response
            print(data)

# --- gather mutlicle call ---
async def fetch(url, session):
    async with session.get(url) as resp:
        data = await resp.text()
        print(f"Finished: {url}")
        return data

async def fetch2():
    urls = ["https://httpbin.org/delay/1", "https://httpbin.org/get"]
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*(fetch(url, session) for url in urls))
        for result in results:
            print(result)

async def fetch3():
    urls = [
        "https://httpbin.org/delay/2",
        "https://httpbin.org/get",
        "https://httpbin.org/uuid"
    ]

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch(url, session))
            tasks.append(task)

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        print("All responses received.")

        # Optional: print results
        for i, result in enumerate(results):
            print(f"Response {i+1}:\n{result[:100]}...\n")  # print first 100 chars


# ============================

if '__name__' == '__main__':
    client1()
    client2()
    asyncio.run(fetch1())
    asyncio.run(fetch2())
    asyncio.run(fetch3())
