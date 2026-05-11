import speech_recognition as sr
import webbrowser

ARIS_URL = "http://127.0.0.1:7000"

recognizer = sr.Recognizer()
mic = sr.Microphone()

print("🎤 ARIS VOICE SYSTEM STARTED")
print("Say: open aris")

def normalize(text):
    text = text.lower()
    text = text.replace(" ", "")
    return text

while True:
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("\nListening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)

        text = recognizer.recognize_google(audio)
        print("Heard RAW:", text)

        cleaned = normalize(text)
        print("Heard CLEAN:", cleaned)

        # 🔥 FLEXIBLE MATCHING (IMPORTANT FIX)
        if "openaris" in cleaned or "openari" in cleaned:
            print("✅ OPEN ARIS DETECTED")
            webbrowser.open(ARIS_URL)

        else:
            print("❌ No match")

    except sr.UnknownValueError:
        print("⚠️ Could not understand audio")

    except Exception as e:
        print("ERROR:", e)