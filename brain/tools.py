import webbrowser

class ToolExecutor:

    def execute(self, tool):

        if tool == "youtube":
            webbrowser.open("https://youtube.com")

        elif tool == "spotify":
            webbrowser.open("https://spotify.com")

        elif tool == "gmail":
            webbrowser.open("https://mail.google.com")

        elif tool == "maps":
            webbrowser.open("https://maps.google.com")

        return f"{tool} executed"