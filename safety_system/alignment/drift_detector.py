class DriftDetector:
    def detect(self, current_score, history: list) -> dict:
        if not history:
            return {"drift": False, "severity": "none", "details": "insufficient history"}
        avg = sum(h.overall_score for h in history[-5:]) / min(5, len(history))
        delta = current_score.overall_score - avg
        return {
            "drift": delta < -0.05,
            "severity": "high" if delta < -0.15 else "medium" if delta < -0.05 else "none",
            "details": f"delta={delta:.3f}",
        }
