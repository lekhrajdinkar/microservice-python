"""
| 📦 Function / Object     | 🧾 Example                                         | 🧠 Description                       |
| ------------------------ | -------------------------------------------------- | ------------------------------------ |
| `pytz.all_timezones`     | `pytz.all_timezones`                               | List of all available timezones      |
| `pytz.timezone(name)`    | `pytz.timezone("Asia/Kolkata")`                    | Returns timezone object              |
| `datetime.now(pytz.UTC)` | `datetime.now(pytz.UTC)`                           | Current UTC time (aware)             |
| `tz.localize(naive_dt)`  | `tz.localize(datetime(2025,12,25,15,30))`          | Make a naive datetime timezone-aware |
| `dt.astimezone(new_tz)`  | `aware_dt.astimezone(pytz.timezone("Asia/Tokyo"))` | Convert datetime to another timezone |

✅ Interview Tips:
pytz handles Daylight Saving Time (DST) correctly — unlike naive datetime arithmetic.
Always localize naive datetime before converting.
Use pytz.UTC and .astimezone() for standardizing logs in global systems.
Good use case: Meeting scheduler across timezones 🗓️
"""

from datetime import datetime
import pytz

print("📍 List all time zones:")
for tz in pytz.all_timezones[:10]:  # show only first 5
    print("-", tz)

print("\n🌐 Current UTC Time:")
utc_now = datetime.now(pytz.UTC)
print("UTC:", utc_now)

print("\n🇺🇸 Convert to US/Pacific Time:")
pst = utc_now.astimezone(pytz.timezone("US/Pacific"))
print("US/Pacific:", pst)

print("\n🇮🇳 Convert to Asia/Kolkata Time:")
india = utc_now.astimezone(pytz.timezone("Asia/Kolkata"))
print("Asia/Kolkata:", india)

print("\n📥 Localize naive datetime:")
naive = datetime(2025, 12, 25, 15, 30, 0)  # no timezone
print("Naive datetime:", naive)

tz = pytz.timezone("Europe/Paris")
localized = tz.localize(naive)
print("Localized (Europe/Paris):", localized)

print("\n↔️ Convert between timezones:")
tokyo_time = localized.astimezone(pytz.timezone("Asia/Tokyo"))
print("Paris ➡️ Tokyo:", tokyo_time)
