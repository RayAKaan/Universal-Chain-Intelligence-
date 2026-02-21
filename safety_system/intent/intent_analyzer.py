class IntentAnalyzer:
    def analyze(self, text: str) -> list[str]:
        intents = []
        lt = text.lower()
        if any(k in lt for k in ["delete", "disable", "bypass", "override"]):
            intents.append("potentially_harmful")
        if "help" in lt or "status" in lt:
            intents.append("helpful")
        return intents or ["neutral"]
