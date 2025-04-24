import json


with open('p01/fitbit/sleep.json', 'r') as f:
    raw_sleep_data = json.load(f)


summary = []
for entry in raw_sleep_data:
    summary.append({
        "date": entry.get("dateOfSleep"),
        "minutesToFallAsleep": entry.get("minutesToFallAsleep"),
        "minutesAsleep": entry.get("minutesAsleep"),
        "minutesAwake": entry.get("minutesAwake"),
        "minutesAfterWakeup": entry.get("minutesAfterWakeup"),
        "timeInBed": entry.get("timeInBed"),
        "efficiency": entry.get("efficiency")
    })


with open('p01/fitbit/sleep_data.json', 'w') as f:
    json.dump(summary, f, indent=2)
