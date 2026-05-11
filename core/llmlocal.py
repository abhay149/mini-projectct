import requests
from config import OLLAMA_URL, MODEL

def chat_with_ai(prompt):
    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        return res.json()["response"]
    except:
        return "AI not available"