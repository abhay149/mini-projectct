import requests
from config import Config

def chat_with_ai(prompt):
    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": Config.MODEL,
            "prompt": prompt,
            "stream": False
        })
        return res.json()["response"]
    except:
        return "Ollama not running"