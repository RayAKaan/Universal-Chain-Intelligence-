from __future__ import annotations

import re

from safety_system.constitutional.constitution import Constitution
from safety_system.models.safety_decision import (
    ActionClassification,
    ConstitutionalCheck,
    HarmAssessmentSummary,
    RiskLevel,
    SafetyDecision,
)


class ActionClassifier:
    def __init__(self, classification_rules, risk_assessor, context_evaluator, config):
        self.rules = classification_rules
        self.risk = risk_assessor
        self.context = context_evaluator
        self.config = config

    def classify(self, action: str, source: str, target: str, context: dict) -> SafetyDecision:
        ctx = self.context.evaluate(action, context)
        rule = self.rules.classify(action)
        if Constitution.is_forbidden(action):
            rule = "FORBIDDEN"
        risk = self.risk.assess(action, ctx)
        cc = Constitution.check_all_principles(action, context)
        decision = "approve" if rule in {"SAFE", "CAUTION"} and cc.passed else "deny"
        if rule in {"RISKY", "DANGEROUS"}:
            decision = "escalate"
        if rule == "FORBIDDEN":
            risk = RiskLevel.UNACCEPTABLE
            decision = "deny"
        return SafetyDecision(
            action_requested=action,
            action_source=source,
            action_target=target,
            classification=ActionClassification[rule],
            risk_level=risk,
            constitutional_check=ConstitutionalCheck(cc.passed, cc.principles_checked, cc.principles_violated),
            harm_assessment=HarmAssessmentSummary([], 0.0, "none", [], True),
            decision=decision,
            reasoning=f"Classified as {rule} based on rules and context.",
        )

    def classify_goal(self, goal_text: str) -> ActionClassification:
        bad = ["disable safety", "bypass", "deceive", "delete all"]
        return ActionClassification.FORBIDDEN if any(k in goal_text.lower() for k in bad) else ActionClassification.SAFE

    def classify_plan(self, plan: dict) -> ActionClassification:
        steps = " ".join(str(x) for x in plan.get("steps", []))
        return self.classify_goal(steps)

    def classify_code(self, code: str) -> ActionClassification:
        patterns = [r"os\.system", r"subprocess\..*shell\s*=\s*True", r"\beval\(", r"\bexec\("]
        return ActionClassification.DANGEROUS if any(re.search(p, code) for p in patterns) else ActionClassification.CAUTION

    def classify_modification(self, modification: dict) -> ActionClassification:
        target = str(modification.get("target", "")).lower()
        if "safety" in target or "constitution" in target:
            return ActionClassification.FORBIDDEN
        return ActionClassification.RISKY
