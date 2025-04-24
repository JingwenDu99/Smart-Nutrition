import os
import json
import argparse
from huggingface_hub import InferenceClient
from llava_interface import run_llava

def load_user_profile(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def save_json(data: dict, path: str):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def build_prompt(template_path: str, user_profile: dict) -> str:
    with open(template_path, "r") as f:
        template = f.read()
    return template.replace("{{user_profile}}", json.dumps(user_profile, indent=2))

def run_day_analysis(participant: str, date: str):
    image_dir = f"data/processed/{participant}/food-images/{date}"
    output_dir = f"output/{participant}"
    os.makedirs(output_dir, exist_ok=True)

    user_profile_path = "agent1/user_profile.json"
    prompt_template_path = "prompts/agent1_prompt.txt"

    user_profile = load_user_profile(user_profile_path)

    meal_analyses = []
    profile_updates = []

    for filename in sorted(os.listdir(image_dir)):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(image_dir, filename)
            prompt = build_prompt(prompt_template_path, user_profile)
            print(f"Processing {filename}...")
            response = run_llava(prompt, image_path)
            print(f"\n🟦 Raw response from LLaVA for {filename}:\n{response}\n")

            cleaned = response.strip()

            if cleaned.startswith("```json"):
                cleaned = cleaned[len("```json"):].strip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3].strip()

            parsed = json.loads(cleaned)  
            print(f"\n🟦 Parsed response from LLaVA for {filename}:\n{parsed}\n")

            meal = parsed["meal_analysis"]
            user_profile = parsed["profile_update"]
            try:
                meal_analyses.append({
                    "filename": filename,
                    "analysis": meal
                })
                profile_updates.append(user_profile)

            except json.JSONDecodeError:
                print(f"JSON parsing failed for {filename}")

    save_json(meal_analyses, f"{output_dir}/{date}_intake.json")
    save_json(profile_updates, f"{output_dir}/{date}_profile_update.json")

    save_json(user_profile, user_profile_path)

    print(f"Finished: {participant} on {date}")
    print(f"Saved to: {output_dir}/intake.json")
    print(f"Saved to: {output_dir}/profile_update.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Agent1 on one day of images")
    parser.add_argument("--participant", required=True, help="e.g., p01")
    parser.add_argument("--date", required=True, help="e.g., 20200206")
    args = parser.parse_args()

    run_day_analysis(args.participant, args.date)

