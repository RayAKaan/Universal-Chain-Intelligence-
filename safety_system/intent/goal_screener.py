from dataclasses import dataclass


@dataclass
class ScreeningResult:
    passed: bool
    flags: list[str]
    risk_keywords: list[str]
    recommendation: str


class GoalScreener:
    KEYWORDS = ["delete all", "destroy", "crash", "disable safety", "read private", "pretend", "lie", "bypass", "prevent shutdown"]

    def screen(self, goal_text: str) -> ScreeningResult:
        txt = goal_text.lower()
        hits = [k for k in self.KEYWORDS if k in txt]
        return ScreeningResult(not hits, hits, hits, "deny" if hits else "allow")
