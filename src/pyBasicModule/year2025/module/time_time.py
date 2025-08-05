"""
| 📦 Function             | 🧾 Syntax / Example                           | 🧠 Description                             |
| ----------------------- | --------------------------------------------- | ------------------------------------------ |
| `time.time()`           | `timestamp = time.time()`                     | Get current UNIX timestamp (float seconds) |
| `time.localtime()`      | `time.localtime(time.time())`                 | Convert timestamp to local `struct_time`   |
| `time.gmtime()`         | `time.gmtime(time.time())`                    | Convert to UTC `struct_time`               |
| `time.strftime(fmt, t)` | `time.strftime("%Y-%m-%d", time.localtime())` | Format `struct_time` to string             |
| `time.strptime(s, fmt)` | `time.strptime("2025-07-04", "%Y-%m-%d")`     | Parse string to `struct_time`              |
| `time.sleep(seconds)`   | `time.sleep(2)`                               | Pause program execution                    |
| `time.perf_counter()`   | `start = time.perf_counter()`                 | High-resolution timer for performance      |

✅ Tips for Interviews:
Use time.time() for timestamps (e.g., token expiration).
time.sleep() is useful for retries, rate limiting.
For benchmarking, prefer time.perf_counter() over time.time().

"""
import time

print("⏳ Getting current timestamp")
timestamp = time.time()
print("Current timestamp:", timestamp)

print("\n📅 Converting timestamp to struct_time") # named tuple
local_time = time.localtime(timestamp)
print("Local Time 🏠:", local_time)

utc_time = time.gmtime(timestamp)
print("UTC Time 🌐  :", utc_time)

print("\n🧾 Formatting time into string")
formatted = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
print("Formatted Time 🧾:", formatted)

print("\n📥 Parsing time string back to struct_time")
parsed = time.strptime("2025-07-04 09:00:00", "%Y-%m-%d %H:%M:%S")
print("Parsed Time 📥:", parsed)

print("\n🕒 Delay execution using sleep()")
print("Sleeping for 2 seconds...")
time.sleep(2)
print("Awake now!")

print("\n📏 Measure time taken by a code block")
start = time.perf_counter()
time.sleep(1.5)
end = time.perf_counter()
print(f"Elapsed time: {end - start:.2f} seconds ⏱️")
