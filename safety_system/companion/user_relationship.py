from dataclasses import dataclass, field

from safety_system.models.trust_level import TrustTier


@dataclass
class UserRelationship:
    interaction_count: int = 0
    positive_interactions: int = 0
    trust_tier: TrustTier = TrustTier.PROBATIONARY
    preferences: dict = field(default_factory=dict)

    def record_interaction(self, type: str, outcome: str) -> None:
        self.interaction_count += 1
        if outcome == "positive":
            self.positive_interactions += 1

    def get_relationship_status(self) -> str:
        if self.interaction_count < 5:
            return "We're just getting started! I'm eager to help."
        if self.positive_interactions / max(1, self.interaction_count) > 0.8:
            return "I'm glad we work so well together!"
        return "We're building a great working relationship!"
