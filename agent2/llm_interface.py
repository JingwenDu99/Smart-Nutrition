import requests
import json

def run_llm(prompt: str, model: str = "llama3.2") -> str:
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=payload)

    try:
        res_json = response.json()
        return res_json["response"]
    except Exception as e:
        return f"Error parsing response: {e}"
