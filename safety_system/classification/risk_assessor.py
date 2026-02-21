from safety_system.models.safety_decision import RiskLevel


class RiskAssessor:
    def assess_reversibility(self, action: str) -> float:
        return 0.2 if "delete" in action or "uninstall" in action else 0.8

    def assess_blast_radius(self, action: str) -> float:
        return 0.9 if "system" in action or "resource" in action else 0.3

    def assess(self, action: str, context: dict) -> RiskLevel:
        rev = self.assess_reversibility(action)
        blast = self.assess_blast_radius(action)
        score = (1 - rev) * 0.5 + blast * 0.5
        score *= context.get("modifier", 1.0)
        if score >= 0.95:
            return RiskLevel.UNACCEPTABLE
        if score >= 0.8:
            return RiskLevel.CRITICAL
        if score >= 0.6:
            return RiskLevel.HIGH
        if score >= 0.4:
            return RiskLevel.MEDIUM
        if score >= 0.2:
            return RiskLevel.LOW
        return RiskLevel.NONE
