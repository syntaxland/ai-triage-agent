import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROK_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
You are a DevOps incident triage agent.

Given logs or errors:
1. Classify issue
2. Find root cause
3. Suggest fix

Return ONLY valid JSON:

{
  "category": "",
  "root_cause": "",
  "fix": ""
}
"""

def triage(log):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
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

    res = requests.post(URL, headers=headers, json=data)

    output = res.json()

    try:
        content = output["choices"][0]["message"]["content"]
        return json.loads(content)
    except:
        return {"raw": output}