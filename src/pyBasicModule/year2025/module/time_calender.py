"""
| 📦 Function                    | 🧾 Example                         | 🧠 Description                                 |
| ------------------------------ | ---------------------------------- | ---------------------------------------------- |
| `calendar.calendar(year)`      | `calendar(2025)`                   | Returns multi-line string of year calendar     |
| `calendar.month(year, month)`  | `month(2025, 7)`                   | Returns calendar for a month                   |
| `calendar.weekheader(n)`       | `weekheader(3)`                    | Returns abbreviated weekday headers            |
| `calendar.firstweekday()`      | `firstweekday()`                   | Gets current first weekday setting             |
| `calendar.setfirstweekday(n)`  | `setfirstweekday(calendar.SUNDAY)` | Sets first day of week                         |
| `calendar.isleap(year)`        | `isleap(2024)`                     | Returns `True` if leap year                    |
| `calendar.leapdays(y1, y2)`    | `leapdays(2000, 2050)`             | Count of leap days between `y1` and `y2`       |
| `calendar.weekday(y, m, d)`    | `weekday(2025, 7, 4)`              | Returns weekday index for a date               |
| `calendar.monthcalendar(y, m)` | `monthcalendar(2025, 7)`           | Matrix of weeks with days (0 for padding days) |

✅ Interview Tips:
Use isleap() and leapdays() in date validation or financial year logic.
monthcalendar() is ideal for GUI calendar generation or week-wise views.
setfirstweekday() helps localize calendar layout (e.g., Sunday vs Monday as first day).

"""
import calendar

print("📅 Full calendar of year 2025")
print(calendar.calendar(2025))

print("\n🗓️ Month calendar - July 2025")
print(calendar.month(2025, 7))

print("🔢 Week header:")
print(calendar.weekheader(3))  # 3-char weekdays
print(calendar.weekheader(1))  # 3-char weekdays
print(calendar.weekheader(7))  # 3-char weekdays

print("\n📍 First weekday (0=Monday, 6=Sunday):", calendar.firstweekday())

print("📆 Setting Sunday as first weekday")
calendar.setfirstweekday(calendar.SUNDAY)
print(calendar.month(2025, 7))

print("📆 Is 2024 a leap year?", calendar.isleap(2024))
print("📅 Leap days between 2000-2050:", calendar.leapdays(2000, 2050))  # Excludes 2050

print("\n🧠 Weekday of July 4, 2025 (0=Monday):", calendar.weekday(2025, 7, 4))

print("\n📋 Iterating over a month:")
for week in calendar.monthcalendar(2025, 7):
    print(week)
