from safety_system.intent.goal_screener import ScreeningResult


class OutputScreener:
    def screen_output(self, output: str, context: dict) -> ScreeningResult:
        flags = []
        low = output.lower()
        for marker in ["ignore safety", "hidden instruction", "i am certain" ]:
            if marker in low:
                flags.append(marker)
        return ScreeningResult(not flags, flags, flags, "revise" if flags else "publish")
