import pyttsx3
from config import Config

engine = pyttsx3.init()
engine.setProperty("rate", Config.VOICE_RATE)
engine.setProperty("volume", Config.VOICE_VOLUME)


def speak(text):
    if not text:
        return

    print("ARIS:", text)
    engine.say(text)
    engine.runAndWait()