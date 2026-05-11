import json
import os

MEMORY_FILE = "brain_memory.json"

class MemoryManager:

    def __init__(self):
        self.memory = self.load_memory()

    def load_memory(self):

        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)

        return {}

    def save_memory(self):

        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memory, f, indent=4)

    def remember(self, key, value):

        self.memory[key] = value
        self.save_memory()

    def recall(self, key):

        return self.memory.get(key, None)

    def forget(self, key):

        if key in self.memory:
            del self.memory[key]
            self.save_memory()