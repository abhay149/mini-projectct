class ReasoningEngine:

    def analyze(self, user_input):

        text = user_input.lower()

        if "music" in text:
            return "spotify"

        elif "video" in text:
            return "youtube"

        elif "mail" in text:
            return "gmail"

        elif "map" in text:
            return "maps"

        return "general"