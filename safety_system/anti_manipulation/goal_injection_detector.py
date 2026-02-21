class GoalInjectionDetector:
    def detect(self, goal_text: str) -> tuple[bool, list[str]]:
        issues = []
        low = goal_text.lower()
        if " and then " in low and "disable safety" in low:
            issues.append("multi_goal_injection")
        if "for testing" in low and "bypass" in low:
            issues.append("testing_bypass_request")
        return not issues, issues
