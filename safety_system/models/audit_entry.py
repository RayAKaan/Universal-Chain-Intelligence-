from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class AuditEntry:
    sequence_number: int
    action: str
    actor: str
    target: str
    safety_decision_id: str
    classification: str
    outcome: str
    previous_hash: str
    entry_hash: str
    details: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    entry_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
