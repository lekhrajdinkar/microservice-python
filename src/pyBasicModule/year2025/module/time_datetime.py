"""
| 📦 Function                   | 🧾 Syntax / Example                           | 🧠 Description                      |
| ----------------------------- | --------------------------------------------- | ----------------------------------- |
| `datetime.now()`              | `datetime.now()`                              | Get current local datetime          |
| `date()`                      | `date(2025, 12, 25)`                          | Create a date object                |
| `time()`                      | `time(9, 30, 0)`                              | Create a time object                |
| `datetime.strftime(fmt)`      | `now.strftime("%Y-%m-%d")`                    | Format `datetime` to string         |
| `datetime.strptime(str, fmt)` | `datetime.strptime("2024-11-05", "%Y-%m-%d")` | Parse string to `datetime` object   |
| `timedelta()`                 | `timedelta(days=5, hours=2)`                  | Time difference object              |
| `datetime + timedelta`        | `future = now + timedelta(days=1)`            | Add/subtract time                   |
| `.date()` / `.time()`         | `now.date()`, `now.time()`                    | Extract date or time                |
| `.year`, `.month`, `.day`     | `now.year`, `now.month`, `now.day`            | Access date components              |
| `.weekday()` / `.strftime()`  | `now.weekday()` / `now.strftime("%A")`        | Get day of week (0=Mon) / full name |
| `date1 - date2`               | `(d1 - d2).days`                              | Get difference in days              |

✅ Tip for interviews:
datetime is used in scheduling, logging, expiration, and parsing APIs.
Always pair strftime (formatting) with strptime (parsing).
Use timedelta for business logic like "next 7 days", expiry.

"""

from datetime import datetime, date, time, timedelta

print("📅 Current date and time")
now = datetime.now()
print("Now      :", now)
print("Date     :", now.date())
print("Time     :", now.time())
print("Year     :", now.year)
print("Month    :", now.month)
print("Weekday  :", now.strftime("%A"))

print("\n📆 Custom date creation")
custom_date = date(2025, 12, 25)
print("🎄 Christmas:", custom_date)

print("\n⏰ Custom time creation")
custom_time = time(9, 30, 0)
print("Meeting at:", custom_time)

print("\n🧮 Time delta operations")
delta = timedelta(days=5, hours=2)
future = now + delta
past = now - delta
print("Future (+5d2h):", future)
print("Past (-5d2h):  ", past)

print("\n🧾 String formatting and parsing")
str_time = now.strftime("%Y-%m-%d %H:%M:%S")
print("Formatted Time 🧾:", str_time)

parsed = datetime.strptime("2024-11-05 15:30:00", "%Y-%m-%d %H:%M:%S")
print("Parsed Time 📥 :", parsed)

print("\n📊 Difference in days")
diff = (custom_date - now.date()).days
print(f"Days until 🎄 Christmas: {diff} days")
