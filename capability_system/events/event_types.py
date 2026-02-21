from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from capability_system.utils.hashing import generate_id


class EventType(str, Enum):
    CAPABILITY_DISCOVERED = "CAPABILITY_DISCOVERED"
    CAPABILITY_REGISTERED = "CAPABILITY_REGISTERED"
    CAPABILITY_UPDATED = "CAPABILITY_UPDATED"
    CAPABILITY_ACTIVATED = "CAPABILITY_ACTIVATED"
    CAPABILITY_DEACTIVATED = "CAPABILITY_DEACTIVATED"
    CAPABILITY_DEPRECATED = "CAPABILITY_DEPRECATED"
    CAPABILITY_REMOVED = "CAPABILITY_REMOVED"
    CAPABILITY_BENCHMARKED = "CAPABILITY_BENCHMARKED"
    CAPABILITY_HEALTH_CHANGED = "CAPABILITY_HEALTH_CHANGED"
    CAPABILITY_STATE_CHANGED = "CAPABILITY_STATE_CHANGED"
    DISCOVERY_SCAN_STARTED = "DISCOVERY_SCAN_STARTED"
    DISCOVERY_SCAN_COMPLETED = "DISCOVERY_SCAN_COMPLETED"
    BENCHMARK_STARTED = "BENCHMARK_STARTED"
    BENCHMARK_COMPLETED = "BENCHMARK_COMPLETED"
    REGISTRY_IMPORTED = "REGISTRY_IMPORTED"
    REGISTRY_EXPORTED = "REGISTRY_EXPORTED"


@dataclass
class Event:
    event_type: EventType
    source: str
    data: dict
    event_id: str = field(default_factory=generate_id)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
