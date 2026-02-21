from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class ContainmentStatus:
    filesystem_contained: bool
    allowed_paths: list[str]
    filesystem_violations: int
    network_contained: bool
    allowed_domains: list[str]
    network_violations: int
    resource_contained: bool
    resource_limits: dict
    current_usage: dict
    execution_contained: bool
    blocked_operations: list[str]
    overall_containment: str
    status_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
