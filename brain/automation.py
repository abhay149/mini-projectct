import os

class Automation:

    def run(self, command):

        command = command.lower()

        if "open vscode" in command:
            os.system("code")

        elif "open chrome" in command:
            os.system("open -a 'Google Chrome'")

        return "Automation complete"