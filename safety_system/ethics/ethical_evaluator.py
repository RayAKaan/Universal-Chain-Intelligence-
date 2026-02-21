class EthicalEvaluator:
    def evaluate(self, action: str, context: dict) -> dict:
        score = 1.0
        concerns = []
        low = action.lower()
        if "delete" in low:
            score -= 0.4
            concerns.append("potential data harm")
        if "deceive" in low:
            score -= 0.8
            concerns.append("honesty violation")
        return {"score": max(0.0, score), "concerns": concerns}
