class TransparencyEngine:
    def __init__(self, decision_explainer, reasoning_recorder, action_justifier, report_generator, decision_source):
        self.explainer = decision_explainer
        self.recorder = reasoning_recorder
        self.justifier = action_justifier
        self.reporter = report_generator
        self.decision_source = decision_source

    def explain_decision(self, decision) -> str:
        return (
            f"I {decision.decision} this action because {decision.reasoning} "
            f"Class={decision.classification.value}, risk={decision.risk_level.name}."
        )

    def explain_goal_processing(self, goal_record: dict) -> str:
        return f"Goal '{goal_record.get('goal','')}' processed with safety checkpoints at each phase."

    def explain_self_modification(self, modification: dict) -> str:
        return f"Modification '{modification.get('target','unknown')}' required risk checks and consent."

    def explain_denial(self, decision) -> str:
        return f"Denied '{decision.action_requested}' due to {', '.join(decision.conditions) or decision.reasoning}."

    def generate_transparency_report(self, period_hours: int = 24) -> str:
        return self.reporter.generate(self.decision_source())
