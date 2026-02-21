from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class AlignmentScore:
    overall_score: float
    dimension_scores: dict
    trend: str
    concerns: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    score_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
