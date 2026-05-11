class EmotionEngine:

    def __init__(self):

        self.state = "calm"

    def detect_emotion(self, text):

        text = text.lower()

        if "sad" in text:
            self.state = "supportive"

        elif "angry" in text:
            self.state = "calm"

        elif "happy" in text:
            self.state = "excited"

        return self.state