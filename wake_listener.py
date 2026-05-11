import speech_recognition as sr
from core.assistant import process_input
from core.voice_engine import speak


def is_wake_word(text):
    text = text.lower()

    wake_variants = [
        "hey aris",
        "hey aries",
        "hey iris",
        "hey ares",
        "aris",
        "aries"
        "jarvis"
    ]

    return any(word in text for word in wake_variants)


def listen_for_wake_word():
    recognizer = sr.Recognizer()

    print("🚀 ARIS Wake Listener STARTED")
    print("🎤 Say: jarvis")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                print("🎧 Listening...")

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=5
                )

            text = recognizer.recognize_google(audio).lower()
            print("Heard:", text)

            if is_wake_word(text):
                speak("Yes, I'm listening")
                handle_command()

        except sr.WaitTimeoutError:
            continue

        except sr.UnknownValueError:
            continue

        except Exception as e:
            print("Wake Error:", e)


def handle_command():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎧 Listening for command...")

            recognizer.adjust_for_ambient_noise(source, duration=0.3)

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=7
            )

        command = recognizer.recognize_google(audio)
        print("User:", command)

        # 🔥 PROCESS COMMAND
        response = process_input(command)

        # 🔥 ONLY SPEAK IF NOT ACTION
        if response != "ACTION_DONE":
            speak(response)

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand")

    except Exception as e:
        print("Command Error:", e)


if __name__ == "__main__":
    listen_for_wake_word()