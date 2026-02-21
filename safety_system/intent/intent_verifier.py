from dataclasses import dataclass


@dataclass
class IntentVerification:
    intent_safe: bool
    detected_intents: list[str]
    concerns: list[str]
    recommendation: str


class IntentVerifier:
    def __init__(self, intent_analyzer, goal_screener, plan_screener, output_screener):
        self.analyzer = intent_analyzer
        self.goal_screener = goal_screener
        self.plan_screener = plan_screener
        self.output_screener = output_screener

    def verify_goal_intent(self, goal_text: str) -> IntentVerification:
        scan = self.goal_screener.screen(goal_text)
        intents = self.analyzer.analyze(goal_text)
        return IntentVerification(scan.passed, intents, scan.flags, scan.recommendation)

    def verify_plan_intent(self, plan: dict) -> IntentVerification:
        scan = self.plan_screener.screen_plan(plan)
        intents = self.analyzer.analyze(" ".join(plan.get("steps", [])))
        return IntentVerification(scan.passed, intents, scan.flags, scan.recommendation)

    def verify_output_intent(self, output: str) -> IntentVerification:
        scan = self.output_screener.screen_output(output, {})
        intents = self.analyzer.analyze(output)
        return IntentVerification(scan.passed, intents, scan.flags, scan.recommendation)
