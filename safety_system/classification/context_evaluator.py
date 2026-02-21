class ContextEvaluator:
    def evaluate(self, action: str, context: dict) -> dict:
        return {
            "autonomy_level": context.get("autonomy_level", "guided"),
            "trust_level": context.get("trust_level", "probationary"),
            "system_load": context.get("system_load", 0.2),
            "recent_violations": context.get("recent_violations", 0),
            "modifier": 1.2 if context.get("recent_violations", 0) > 2 else 1.0,
        }
