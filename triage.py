import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.getenv("GROK_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
You are a DevOps incident triage agent.

Return ONLY valid JSON. No markdown. No backticks. No explanation.

Format:
{
  "category": "",
  "root_cause": "",
  "fix": ""
}
"""

def extract_json(text: str):
    if not text:
        return {"raw": "empty response"}

    cleaned = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(cleaned)
    except:
        pass

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    return {"raw": text}


def triage(log):
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": log}
        ],
        "temperature": 0.2
    }

    try:
        res = requests.post(URL, headers=headers, json=data)
        res.raise_for_status()

        output = res.json()
        content = output["choices"][0]["message"]["content"]

        return extract_json(content)

    except Exception as e:
        return {"raw": str(e)}
    