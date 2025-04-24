import base64
import requests
import json

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def run_llava(prompt: str, image_path: str) -> str:
    url = "http://localhost:11434/api/generate"
    image_base64 = encode_image_to_base64(image_path)

    payload = {
        "model": "llava",
        "prompt": prompt,
        "images": [image_base64],
        "stream": False
    }

    response = requests.post(url, json=payload)

    try:
        res_json = response.json()
        return res_json["response"]
    except Exception as e:
        return f"Error parsing response: {e}"

