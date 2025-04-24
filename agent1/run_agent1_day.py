import os
import json
import argparse
from huggingface_hub import InferenceClient
from llava_interface import run_llava
import copy

def load_user_profile(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def save_json(data: dict, path: str):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def parse_llava_json(text):
    """
    Clean up and parse LLaVA-style JSON string (may be wrapped in triple backticks)
    """
    import json
    if isinstance(text, str):
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
        return json.loads(text)
    return text 

def build_prompt(template_path: str, user_profile: dict) -> str:
    with open(template_path, "r") as f:
        template = f.read()
    return template.replace("{{user_profile}}", json.dumps(user_profile, indent=2))

def run_day_analysis(participant: str, date: str):
    image_dir = f"data/processed/{participant}/food-images/{date}"
    output_dir = f"output/{participant}"
    os.makedirs(output_dir, exist_ok=True)

    user_profile_path = "agent1/user_profile.json"
    prompt1_template_path = "prompts/agent1_prompt1.txt" 
    prompt2_template_path = "prompts/agent1_prompt2.txt"

    user_profile = load_user_profile(user_profile_path)

    meal_analyses = []
    profile_updates = []

    for filename in sorted(os.listdir(image_dir)):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(image_dir, filename)
            prompt2 = build_prompt(prompt2_template_path, user_profile)
            print(f"Processing {filename}...")
            with open(prompt1_template_path, "r") as f:
                prompt1 = f.read()
            response1 = run_llava(prompt1, image_path)
            response2 = run_llava(prompt2, image_path)
            print(f"\n🟦 Raw meal analysis from LLaVA for {filename}:\n{response1}\n")

            print(f"\n🟦 Raw profile update from LLaVA for {filename}:\n{response2}\n")
       
            try:
                meal_analyses.append({
                    "filename": filename,
                    "analysis": parse_llava_json(response1)
                })
                user_profile = parse_llava_json(response2)
                profile_updates.append({
                    "filename": filename,
                    "updated_profile": copy.deepcopy(user_profile)  # snapshot of updated profile for this meal
                })

            except json.JSONDecodeError:
                print(f"JSON parsing failed for {filename}")

    save_json(meal_analyses, f"{output_dir}/{date}_intake.json")
    save_json(profile_updates, f"{output_dir}/{date}_profile_update.json")
    save_json(user_profile, user_profile_path)

    print(f"Saved to: {output_dir}/intake.json")
    print(f"Saved to: {output_dir}/profile_update.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Agent1 on one day of images")
    parser.add_argument("--participant", required=True, help="e.g., p01")
    parser.add_argument("--date", required=True, help="e.g., 2020-02-06")
    args = parser.parse_args()

    run_day_analysis(args.participant, args.date)

