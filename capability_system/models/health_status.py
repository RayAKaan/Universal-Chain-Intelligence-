from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from capability_system.models.capability import HealthStatus


@dataclass
class CapabilityHealth:
    capability_id: str
    status: HealthStatus
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: str = ""
