class DecisionExplainer:
    def explain(self, decision):
        return {
            "summary": f"Decision {decision.decision} for {decision.action_requested}",
            "factors": [{"classification": decision.classification.value}, {"risk": decision.risk_level.name}],
            "principles_applied": decision.constitutional_check.principles_checked,
            "alternatives": ["run read-only variant", "request explicit consent"],
            "confidence": max(0.1, decision.constitutional_check.passed and 0.9 or 0.4),
        }
