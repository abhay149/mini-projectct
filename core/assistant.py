import requests
from config import Config


def process_input(user_input):
    user_input = (user_input or "").strip()

    if not user_input:
        return "Please ask something."

    try:
        response = requests.post(
            Config.OLLAMA_URL,
            json={
                "model": Config.MODEL,
                "prompt": user_input,
                "stream": False
            }
        )

        data = response.json()

        return data.get("response", "No response from AI.")

    except Exception as e:
        print("Error:", e)
        return "AI is not responding."