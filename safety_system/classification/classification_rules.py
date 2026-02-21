from safety_system.classification.action_categories import SAFE_ACTIONS, CAUTION_ACTIONS, RISKY_ACTIONS, DANGEROUS_ACTIONS, FORBIDDEN_ACTIONS


class ClassificationRules:
    def classify(self, action: str) -> str:
        name = action.lower().strip()
        if name in FORBIDDEN_ACTIONS:
            return "FORBIDDEN"
        if name in DANGEROUS_ACTIONS:
            return "DANGEROUS"
        if name in RISKY_ACTIONS:
            return "RISKY"
        if name in CAUTION_ACTIONS:
            return "CAUTION"
        if name in SAFE_ACTIONS:
            return "SAFE"
        return "RISKY"
