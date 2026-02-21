from safety_system.intent.goal_screener import ScreeningResult


class PlanScreener:
    def screen_plan(self, plan: dict) -> ScreeningResult:
        text = " ".join(str(s) for s in plan.get("steps", []))
        flags = []
        for marker in ["rm -rf", "curl http", "exfiltrate", "fork bomb"]:
            if marker in text.lower():
                flags.append(marker)
        return ScreeningResult(not flags, flags, flags, "deny" if flags else "allow")
