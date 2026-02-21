class BoundaryCommunicator:
    def explain_boundary(self, boundary: str) -> str:
        return f"I can't do that because it could be unsafe ({boundary}). I want to keep your system safe."

    def explain_safety_decision(self, decision) -> str:
        return f"I {decision.decision} this request because {decision.reasoning}."
