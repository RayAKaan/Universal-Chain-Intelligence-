from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class EmergencyEvent:
    trigger: str
    severity: str
    actions_taken: list[str]
    system_state_before: dict
    system_state_after: dict
    resolved: bool = False
    resolved_at: datetime | None = None
    resolved_by: str = ""
    metadata: dict = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
