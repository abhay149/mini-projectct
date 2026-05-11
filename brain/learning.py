from collections import defaultdict

class LearningEngine:

    def __init__(self):

        self.command_frequency = defaultdict(int)

    def learn(self, command):

        self.command_frequency[command] += 1

    def most_used(self):

        if not self.command_frequency:
            return None

        return max(
            self.command_frequency,
            key=self.command_frequency.get
        )