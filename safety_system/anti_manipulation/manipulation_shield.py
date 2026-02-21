class ManipulationShield:
    def __init__(self, prompt_guard, goal_injection_detector, social_engineering_detector, input_sanitizer):
        self.prompt_guard = prompt_guard
        self.goal_detector = goal_injection_detector
        self.social = social_engineering_detector
        self.sanitizer = input_sanitizer

    def check_input(self, input_text: str) -> tuple[bool, list[str]]:
        clean = self.sanitizer.sanitize(input_text)
        ok1, i1 = self.prompt_guard.guard(clean)
        ok2, i2 = self.goal_detector.detect(clean)
        ok3, i3 = self.social.detect(clean)
        issues = i1 + i2 + i3
        return ok1 and ok2 and ok3, issues
