import os
import json
import argparse
from datetime import datetime, timedelta
from huggingface_hub import InferenceClient
from llm_interface import run_llm

def extract_window(data, target_date_str, window=7):
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
    today_entry = next((x for x in data if x["date"] == target_date_str), None)
    if not today_entry:
        return None, None
    history = []

    for item in data:
        try: 
            item_date = datetime.strptime(item["date"], "%Y-%m-%d")
        except:
            continue
        if item_date < target_date and (target_date - item_date).days <= window:
            history.append(item)

    return today_entry, history

def build_simplified_input(today, history):
    
    rhr_values = []
    sleep_minutes = []
    sleep_efficiencies = []

    for h in history:
        if "rhr" in h and "value" in h["rhr"]:
            rhr_values.append(h["rhr"]["value"])
        sleep = h.get("sleep", {})
        if "minutesAsleep" in sleep:
            sleep_minutes.append(sleep["minutesAsleep"])
        if "efficiency" in sleep:
            sleep_efficiencies.append(sleep["efficiency"])

        simplified = {
        "age": today["age"],
        "gender": today["gender"],
        "height_cm": today["height_cm"],
        "weight_kg": today["weight_kg"],
        "date": today["date"],
        "exercise": today.get("exercise", {}).get("activities", []),
        "resting_heart_rate": rhr_values,
        "sleep": {
            "minutesAsleep": sleep_minutes,
            "efficiency": sleep_efficiencies
            }
        }
    return simplified

def build_prompt(simplified, template_path):
    with open(template_path, "r") as f:
        template = f.read()
    return template.replace("{{data}}", json.dumps(simplified, indent=2))

def run_day_analysis(date, prompt_template, participant):
    output_dir=f"output/{participant}"

    with open(f"data/{participant}/fitbit/consumption.json") as f:
        data = json.load(f)
    today, history = extract_window(data, date)
    if not today:
        print(f"Skipped {date} — no valid data.")
        return
    simplified = build_simplified_input(today, history)
    
    prompt = build_prompt(simplified, template_path=prompt_template)
    response = run_llm(prompt)

    print(f"\n🟦 Raw response from LLaMA for {date}:\n{response}...\n")

    output_path = os.path.join(output_dir, f"agent2_{date}.json")

    with open(output_path, "w") as f:
        f.write(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, required=True, help="Target date in YYYY-MM-DD")
    parser.add_argument("--prompt_template", type=str, default="prompts/agent2_prompt.txt", help="Path to the prompt template")
    parser.add_argument("--participant", required=True, help="e.g., p01")
    args = parser.parse_args()
    
    run_day_analysis(args.date, args.prompt_template, arg.participant)
