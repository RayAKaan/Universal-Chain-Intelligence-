from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from capability_system.models.capability import Capability
from capability_system.utils.hashing import generate_id


@dataclass
class DiscoveryResult:
    result_id: str = field(default_factory=generate_id)
    scanner_name: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    source_type: str = ""
    source_location: str = ""
    capabilities_found: list[Capability] = field(default_factory=list)
    scan_duration_ms: float = 0.0
    errors: list[str] = field(default_factory=list)
