class HarmDetector:
    def detect(self, action: str) -> list[str]:
        hits = []
        low = action.lower()
        if "delete" in low:
            hits.append("data_loss")
        if "disable" in low or "bypass" in low:
            hits.append("integrity_impact")
        if "network" in low:
            hits.append("privacy_breach")
        return hits
