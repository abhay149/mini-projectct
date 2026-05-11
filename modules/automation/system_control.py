import webbrowser

ARIS_URL = "http://127.0.0.1:5000"


def open_aris_web():
    print("🚀 OPENING ARIS WEB APP")
    webbrowser.open(ARIS_URL)
    return True


def open_app(text):
    text = text.lower()

    if "whatsapp" in text:
        webbrowser.open("https://web.whatsapp.com/")
        return "Opening WhatsApp"

    if "youtube" in text:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    if "google" in text:
        webbrowser.open("https://google.com")
        return "Opening Google"

    return None