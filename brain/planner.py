class Planner:

    def create_plan(self, task):

        task = task.lower()

        if "study" in task:

            return [
                "Open browser",
                "Search study material",
                "Open notes",
                "Start focus timer"
            ]

        elif "coding" in task:

            return [
                "Open VS Code",
                "Open project folder",
                "Launch terminal"
            ]

        return ["No plan available"]