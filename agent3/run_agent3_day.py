import os
import json
import argparse
from llm_interface import run_llm

def load_json_file(path):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return None
    with open(path) as f:
        return json.load(f)

def build_prompt(date, intake, profile, agent2_summary, prompt_path):
    with open(prompt_path) as f:
        template = f.read()

    return template \
        .replace("{{date}}", date) \
        .replace("{{intake}}", json.dumps(intake, indent=2)) \
        .replace("{{profile}}", json.dumps(profile, indent=2)) \
        .replace("{{agent2_summary}}", json.dumps(agent2_summary, indent=2))

def run_day_analysis(date, intake, profile, agent2_summary, prompt_template, participant):
    output_dir=f"output/{participant}"
    if not all([intake, profile, agent2_summary]):
        print("⚠️ Missing one or more input files. Skipping.")
        return

    prompt = build_prompt(date, intake, profile, agent2_summary, prompt_template)
    response = run_llm(prompt)

    print(f"\n🟦 Raw response from LLaMA for {date}:\n{response}...\n")

    output_path = os.path.join(output_dir, f"agent3_{date}.txt")
    with open(output_path, "w") as f:
        f.write(response)

    print(f"[✓] Saved Agent3 analysis to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, required=True, help="Date in YYYY-MM-DD format")
    parser.add_argument("--prompt_template", type=str, default="prompts/agent3_prompt.txt", help="Prompt template path")
    parser.add_argument("--participant", required=True, help="e.g., p01")
    args = parser.parse_args()

    intake_path = os.path.join(f"output/{args.participant}", f"{args.date}_intake.json")
    profile_path = os.path.join("agent1", "user_profile.json")
    agent2_path = os.path.join(f"output/{args.participant}", f"agent2_{args.date}.json")


    intake = load_json_file(intake_path)
    profile = load_json_file(profile_path)
    agent2 = load_json_file(agent2_path)
    agent2_summary = agent2.get("summary_text", "")

    run_day_analysis(args.date, intake, profile, agent2_summary, args.prompt_template, args.participant)
