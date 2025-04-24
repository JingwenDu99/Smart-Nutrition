# Smart-Nutrition

Smart Nutrition is a multi-agent system powered by LLMs that analyzes smartwatch data and food intake to provide personalized dietary guidance for active individuals. It integrates image-based meal recognition, wearable physiological data, and longitudinal preference tracking to generate real-time nutritional insights.

---

## 🚀 1. Clone the Repository

```bash
git clone https://github.com/your-username/smart-nutrition.git
cd smart-nutrition
```

---

## 🧪 2. Set Up the Virtual Environment

Make sure `conda` is installed (via Miniconda or Anaconda).

Then create and activate the virtual environment :

```bash
conda create -n smart-nutrition python=3.8
conda activate smart-nutrition
```

---

## 🧰 3. Install Dependencies

Install required Python packages:

```bash
pip install pandas requests huggingface_hub
```

This system uses `Ollama` to run local LLMs. You can download `Ollamma` here: https://ollama.com/download, and run the required models:

```bash
ollama run llava
ollama run llama3.2
```

## 📦 4. Raw Data Processing

The raw smartwatch and food data have been included under each participant's folder. Each participant's folder typically includes:

- `food-images/`(photos)
- `sleep.json`
- `resting_heart_rate.json`
- `exercise.json`
- `reporting.csv` (daily weight)

These raw files have been parsed and consolidated using:

```bash
# Align and split food images by timestamp
image_time.json
organize_by_date.py

# Process Fitbit data into per-day structure
process_sleep.py
process_rhr.py
python3 data/generate_consumption.py
```

This will generate:
- `processed/{participant}/food-images` split by date
- `consumption.json` containing daily entries with basic profile, weight (if available), RHR, sleep and exercise

---

## 🗂 5. Code Structure

```
smart-nutrition/
├── agent1/                   # Food image → intake analysis
│   ├── run_agent1_day.py
│   ├── llava_interface.py
│   ├── user_profile.json
├── agent2/                   # Physiological & energy summary
│   ├── run_agent2_day.py
│   ├── llm_interface.py
├── agent3/                   # Final dietary recommendation
│   ├── run_agent3_day.py
│   ├── llm_interface.py
├── data/                     # Processed food and Fitbit data 
│   └── processed/
│       └── {participant}/
│           ├── food-images
│   └── {participant}/
│       └── fitbit/
│           ├── generate_{participant}_consumption.py
├── prompts/                  # Prompt templates
├── output/
│   └── {participant}/        # Stores all generated outputs
│       ├── <date>_intake.json
│       ├── agent2_<date>.json
│       ├── agent3_<date>.txt
└── README.md
```

---

## 🧪 6. How to Run the System

Take participant 1 (`p01`) on `2020-02-01` as an example to run the code:

### Step 1: Run Agent 1-3
```bash
python3 agent1/run_agent1_day.py --participant p01 --date 2020-02-01
python3 agent2/run_agent2_day.py --date 2020-02-01
python3 agent3/run_agent3_day.py --date 2020-02-01
```
---

## ✅ Example Expected Output

The final result will be saved to:

```
output/p01/agent3_2020-02-01.txt
```

Example content:

```
You're in a mild caloric deficit today, which might be suitable for light training recovery, but not for heavy performance days. Sleep quality is consistent, and resting heart rate is stable. You may consider adding a small protein-rich snack in the afternoon to better support recovery. Great job staying consistent!
```

---

## 📌 Notes

- You can test each agent independently.
- Agent 1 relies on food image → intake mapping and may require local image files.
- Agent 2 uses `consumption.json` as consolidated physiological data.
- Agent 3 finalizes the loop with dietary suggestion logic.

For questions or improvements, feel free to open an issue or PR!

---

