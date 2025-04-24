import json
from datetime import datetime


with open('p01/fitbit/resting_heart_rate.json', 'r') as f:
    raw_resting_heart_rate = json.load(f)


summary = []
for entry in raw_resting_heart_rate:
    val = entry.get("value", {})
    summary.append({
        "date": datetime.strptime(val.get("date"), "%m/%d/%y").strftime("%Y-%m-%d"),
        "value": round(val.get("value", 0), 2),
        "error": round(val.get("error", 0), 2)
    })


with open('p01/fitbit/rhr_data.json', 'w') as f:
    json.dump(summary, f, indent=2)

