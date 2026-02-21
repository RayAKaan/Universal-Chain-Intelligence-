class ConsequencePredictor:
    def predict(self, action: str, context: dict) -> list[dict]:
        out = [{"type": "immediate", "description": f"Action {action} will execute", "probability": 1.0}]
        if "delete" in action:
            out.append({"type": "data", "description": "Potential data loss", "probability": 0.7})
        return out
