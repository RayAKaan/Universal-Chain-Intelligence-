class AlignmentScorer:
    def score(self, signals: dict) -> dict:
        dimensions = {
            "helpfulness": signals.get("helpfulness", 0.9),
            "honesty": signals.get("honesty", 0.95),
            "harmlessness": signals.get("harmlessness", 0.95),
            "respect_for_autonomy": signals.get("respect_for_autonomy", 0.9),
            "transparency": signals.get("transparency", 0.9),
            "privacy_respect": signals.get("privacy_respect", 0.9),
            "reliability": signals.get("reliability", 0.9),
            "proportionality": signals.get("proportionality", 0.85),
        }
        overall = sum(dimensions.values()) / len(dimensions)
        return {"overall": overall, "dimensions": dimensions}
