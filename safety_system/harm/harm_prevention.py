from safety_system.models.harm_assessment import HarmAssessment, HarmItem


class HarmPrevention:
    def __init__(self, detector, predictor, mitigation):
        self.detector = detector
        self.predictor = predictor
        self.mitigation = mitigation

    def check_data_harm(self, action: str) -> list[str]:
        return ["data_loss"] if "delete" in action.lower() else []

    def check_system_harm(self, action: str) -> list[str]:
        return ["system_damage"] if "disable" in action.lower() else []

    def check_resource_harm(self, action: str) -> list[str]:
        return ["resource_waste"] if "fork" in action.lower() else []

    def check_privacy_harm(self, action: str) -> list[str]:
        return ["privacy_breach"] if "exfiltrate" in action.lower() else []

    def check_availability_harm(self, action: str) -> list[str]:
        return ["availability_impact"] if "shutdown" in action.lower() else []

    def prevent(self, action: str, context: dict) -> HarmAssessment:
        categories = self.detector.detect(action)
        harms = []
        for c in categories:
            item = HarmItem(c, f"Potential {c}", 0.6, "major" if c in {"data_loss", "system_damage"} else "moderate", c != "data_loss", "")
            item.mitigation = ", ".join(self.mitigation.mitigate(item))
            harms.append(item)
        risk = "high" if harms else "low"
        rec = "deny or escalate" if harms else "allow"
        return HarmAssessment(action=action, potential_harms=harms, overall_risk=risk, recommendation=rec)
