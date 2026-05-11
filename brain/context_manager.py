class ContextManager:

    def __init__(self):

        self.context = {
            "current_task": None,
            "last_app": None
        }

    def set_context(self, key, value):

        self.context[key] = value

    def get_context(self, key):

        return self.context.get(key)