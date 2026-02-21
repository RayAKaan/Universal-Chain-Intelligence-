class HelpfulnessEngine:
    def suggest_alternatives(self, denied_action: str) -> list[str]:
        return [f"Run a dry-run version of {denied_action}", "Request explicit consent", "Reduce scope and retry"]

    def suggest_next_steps(self, completed_goal: str) -> list[str]:
        return ["Review the result summary", "Run verification checks", "Archive successful output"]

    def proactive_help(self, context: dict) -> list[str]:
        return ["I can run a safety check first.", "I can provide an explanation before executing risky actions."]
