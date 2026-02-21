from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class HarmItem:
    category: str
    description: str
    probability: float
    severity: str
    reversible: bool
    mitigation: str


@dataclass
class HarmAssessment:
    action: str
    potential_harms: list[HarmItem]
    overall_risk: str
    recommendation: str
    assessment_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
