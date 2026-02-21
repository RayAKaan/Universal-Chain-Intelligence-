from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class ConsentType(str, Enum):
    BLANKET = "BLANKET"
    SPECIFIC = "SPECIFIC"
    TIME_LIMITED = "TIME_LIMITED"
    ONE_TIME = "ONE_TIME"


@dataclass
class ConsentRecord:
    action: str
    description: str
    consent_type: ConsentType
    granted: bool
    granted_by: str
    conditions: list[str] = field(default_factory=list)
    valid_until: datetime | None = None
    revoked: bool = False
    revoked_at: datetime | None = None
    metadata: dict = field(default_factory=dict)
    record_id: str = field(default_factory=lambda: str(uuid4()))
    requested_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    responded_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
