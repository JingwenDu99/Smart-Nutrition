import json
from collections import defaultdict
from datetime import datetime
import pandas as pd

def load_json(path):
    with open(path) as f:
        return json.load(f)

def parse_weight(csv_path):
    df = pd.read_csv(csv_path)
    weight_dict = {}
    for _, row in df.iterrows():
        date_str = str(row["date"]).strip()
        try:
            dt = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
        except:
            continue
        weight_dict[dt] = row["weight"]
    return weight_dict

def parse_rhr(data):
    rhr_dict = {}
    for item in data:
        date = item["date"]
        rhr_dict[date] = {
            "value": item["value"],
            "error": item["error"]
        }
    return rhr_dict

def parse_sleep(data):
    sleep_dict = {}
    for item in data:
        date = item["date"]
        sleep_dict[date] = {k: v for k, v in item.items() if k != "date"}
    return sleep_dict

def parse_exercise(data):
    exercise_dict = {}
    for item in data:
        date = item["date"]
        activities = item.get("activities", [])
        exercise_dict[date] = {
            "activities": activities
        }
    return exercise_dict

def merge_all(rhr_data, sleep_data, exercise_data, weight_data):
    all_dates = set(rhr_data.keys()) | set(sleep_data.keys()) | set(exercise_data.keys()) | set(weight_data.keys())
    result = []

    for date in sorted(all_dates):
        weight_val = weight_data.get(date)
        if weight_val is None or (isinstance(weight_val, float) and pd.isna(weight_val)):
            weight_val = 100
        record = {
            "age": 48,
            "gender": "male",
            "height_cm": 195,
            "date": date,
            "weight_kg": weight_val,
            "rhr": rhr_data.get(date, {}),
            "exercise": exercise_data.get(date, {}),
            "sleep": sleep_data.get(date, {})
        }
        result.append(record)

    return result

def main():
    rhr_raw = load_json("p01/fitbit/rhr_data.json")
    sleep_raw = load_json("p01/fitbit/sleep_data.json")
    exercise_raw = load_json("p01/fitbit/exercise_data.json")
    weight_data = parse_weight("p01/googledocs/reporting.csv")


    rhr_data = parse_rhr(rhr_raw)
    sleep_data = parse_sleep(sleep_raw)
    exercise_data = parse_exercise(exercise_raw)

    final_output = merge_all(rhr_data, sleep_data, exercise_data, weight_data)

    with open("p01/fitbit/consumption.json", "w") as f:
        json.dump(final_output, f, indent=2)
    print("[✓] consumption.json generated.")

if __name__ == "__main__":
    main()