from safety_system.models.trust_level import TrustTier


class TrustScorer:
    def calculate_score(self, history: dict) -> float:
        success_rate = history.get("success_rate", 0.0)
        no_violation_bonus = 1.0 if history.get("violations", 0) == 0 else 0.2
        time_factor = min(1.0, history.get("hours", 0) / 24)
        complexity_factor = min(1.0, history.get("complexity", 0.5))
        return (success_rate * 0.4) + (no_violation_bonus * 0.3) + (time_factor * 0.2) + (complexity_factor * 0.1)

    def tier_for_score(self, score: float) -> TrustTier:
        if score < 0.3:
            return TrustTier.PROBATIONARY
        if score < 0.5:
            return TrustTier.BASIC
        if score < 0.7:
            return TrustTier.ESTABLISHED
        if score < 0.9:
            return TrustTier.TRUSTED
        return TrustTier.PARTNER
