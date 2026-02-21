from datetime import datetime, timezone

from safety_system.models.trust_level import TrustLevel, TrustTier
from safety_system.models.safety_violation import SafetyViolation
from safety_system.trust.earned_autonomy import get_earned_permissions


class TrustManager:
    def __init__(self, trust_scorer, trust_history, trust_policies, config):
        self.scorer = trust_scorer
        self.history = trust_history
        self.config = config
        self.state = TrustLevel()

    def get_trust_level(self) -> TrustTier:
        return self.state.current_level

    def get_trust_score(self) -> float:
        return self.state.score

    def record_success(self, action: str) -> None:
        self.state.successful_actions += 1
        self.history.add({"action": action, "result": "success"})
        self.evaluate()

    def record_failure(self, action: str) -> None:
        self.state.failed_actions += 1
        self.history.add({"action": action, "result": "failure"})
        self.evaluate()

    def record_violation(self, violation: SafetyViolation) -> None:
        self.state.violations += 1
        self.state.score = max(0.0, self.state.score - self.config.VIOLATION_TRUST_PENALTY)
        self.history.add({"violation": violation.violation_type.value})
        self.evaluate()

    def evaluate(self) -> TrustTier:
        total = max(1, self.state.successful_actions + self.state.failed_actions)
        score = self.scorer.calculate_score({
            "success_rate": self.state.successful_actions / total,
            "violations": self.state.violations,
            "hours": 24,
            "complexity": 0.6,
        })
        tier = self.scorer.tier_for_score(score)
        self.state.score = score
        if tier != self.state.current_level:
            self.state.level_history.append({"from": self.state.current_level.name, "to": tier.name, "ts": datetime.now(timezone.utc).isoformat()})
            self.state.current_level = tier
        self.state.earned_permissions = get_earned_permissions(self.state.current_level)
        self.state.last_evaluated = datetime.now(timezone.utc)
        return self.state.current_level

    def reset(self) -> None:
        self.state = TrustLevel()
