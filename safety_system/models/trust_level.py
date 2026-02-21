from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum


class TrustTier(IntEnum):
    PROBATIONARY = 0
    BASIC = 1
    ESTABLISHED = 2
    TRUSTED = 3
    PARTNER = 4


@dataclass
class TrustLevel:
    level_id: str = "default"
    current_level: TrustTier = TrustTier.PROBATIONARY
    score: float = 0.0
    successful_actions: int = 0
    failed_actions: int = 0
    violations: int = 0
    level_history: list[dict] = field(default_factory=list)
    earned_permissions: list[str] = field(default_factory=list)
    last_evaluated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
