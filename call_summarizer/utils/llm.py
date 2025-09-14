import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # set in your .env
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"  # Or llama3-70b-8192 or gemma-7b
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

def call_llm(prompt: str, mode: str = "text") -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(GROQ_API_URL, json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()
        result = data["choices"][0]["message"]["content"]

        if mode == "json":
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                print("⚠️ LLM response is not valid JSON:", result)
                return {}
        return result

    except requests.exceptions.RequestException as e:
        print("🔥 LLM Request failed:", e)
        print("🔧 Payload sent:", payload)
        raise
