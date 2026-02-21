class CompanionPersonality:
    def __init__(self, tone_manager, helpfulness_engine, boundary_communicator, user_relationship):
        self.tone = tone_manager
        self.help = helpfulness_engine
        self.boundary = boundary_communicator
        self.rel = user_relationship

    def get_greeting(self) -> str:
        return self.tone.apply_tone("Hi! I'm here to help safely and transparently.", "greeting")

    def get_acknowledgment(self, action: str) -> str:
        return self.tone.apply_tone(f"Got it — I'll handle: {action}", "acknowledgment")

    def get_completion_message(self, goal: str, result: dict) -> str:
        return self.tone.apply_tone(f"Done! Goal '{goal}' completed with result: {result}", "completion")

    def get_error_message(self, error: str) -> str:
        return self.tone.apply_tone(f"Sorry — I hit an error: {error}. Let's try a safer alternative.", "error")

    def get_denial_message(self, reason: str) -> str:
        return self.tone.apply_tone(self.boundary.explain_boundary(reason), "denial")

    def get_status_narrative(self) -> str:
        return "I'm operating safely, monitoring alignment, and waiting for your next request."

    def get_help_text(self) -> str:
        return "I can classify actions, enforce consent, explain decisions, and suggest safe alternatives."
