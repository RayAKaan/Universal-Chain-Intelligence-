from __future__ import annotations

import logging
import threading
from collections import Counter
from datetime import datetime, timezone

from capability_system.events.event_types import Event, EventType
from capability_system.models.capability import Capability, CapabilityState, CapabilityType, HealthStatus, PerformanceProfile
from capability_system.registry.capability_index import CapabilityIndex
from capability_system.registry.capability_schema import validate_capability
from capability_system.registry.capability_store import CapabilityStore
from capability_system.utils.hashing import generate_fingerprint


class CapabilityRegistry:
    def __init__(self, store: CapabilityStore, event_bus=None):
        self.logger = logging.getLogger("capability_system.registry")
        self.store = store
        self.event_bus = event_bus
        self._lock = threading.RLock()
        self.index = CapabilityIndex()
        self.index.rebuild_from(self.store.load_all())

    def _emit(self, t: EventType, data: dict) -> None:
        if self.event_bus:
            self.event_bus.publish(Event(event_type=t, source="registry", data=data))

    def register(self, capability: Capability) -> str:
        with self._lock:
            validate_capability(capability)
            for existing in self.index.by_id.values():
                if (existing.name == capability.name and existing.version == capability.version) or existing.fingerprint == capability.fingerprint:
                    return existing.capability_id
            capability.state = CapabilityState.REGISTERED
            capability.updated_at = datetime.now(timezone.utc)
            capability.fingerprint = generate_fingerprint(capability)
            self.store.save(capability)
            self.index.add(capability)
            self._emit(EventType.CAPABILITY_REGISTERED, {"capability_id": capability.capability_id})
            return capability.capability_id

    def unregister(self, capability_id: str) -> bool:
        cap = self.get(capability_id)
        cap.state = CapabilityState.REMOVED
        self.update(capability_id, {"state": CapabilityState.REMOVED.value})
        self._emit(EventType.CAPABILITY_REMOVED, {"capability_id": capability_id})
        return True

    def update(self, capability_id: str, updates: dict) -> Capability:
        with self._lock:
            cap = self.get(capability_id)
            for k, v in updates.items():
                if hasattr(cap, k):
                    if k in {"state", "health_status", "capability_type", "execution_type"} and hasattr(type(getattr(cap, k)), "__mro__"):
                        enum_cls = type(getattr(cap, k))
                        v = enum_cls(v) if isinstance(v, str) else v
                    setattr(cap, k, v)
            cap.updated_at = datetime.now(timezone.utc)
            cap.fingerprint = generate_fingerprint(cap)
            self.store.save(cap)
            self.index.update(cap)
            self._emit(EventType.CAPABILITY_UPDATED, {"capability_id": capability_id, "updates": updates})
            return cap

    def get(self, capability_id: str) -> Capability:
        cap = self.index.by_id.get(capability_id)
        if not cap:
            raise KeyError(capability_id)
        return cap

    def get_by_name(self, name: str, version: str | None = None) -> Capability | None:
        for cap in self.index.by_name.get(name, []):
            if version is None or cap.version == version:
                return cap
        return None

    def get_all(self) -> list[Capability]:
        return list(self.index.by_id.values())

    def get_by_type(self, capability_type: CapabilityType) -> list[Capability]:
        return list(self.index.by_type.get(capability_type.value, []))

    def get_by_category(self, category: str) -> list[Capability]:
        return list(self.index.by_category.get(category, []))

    def get_by_state(self, state: CapabilityState) -> list[Capability]:
        return list(self.index.by_state.get(state.value, []))

    def get_active(self) -> list[Capability]:
        return [c for c in self.get_all() if c.state == CapabilityState.ACTIVE and c.is_enabled]

    def exists(self, capability_id: str) -> bool:
        return capability_id in self.index.by_id

    def count(self) -> int:
        return len(self.index.by_id)

    def count_by_state(self) -> dict[CapabilityState, int]:
        cnt = Counter(c.state for c in self.get_all())
        return dict(cnt)

    def activate(self, capability_id: str) -> bool:
        self.update(capability_id, {"state": CapabilityState.ACTIVE.value, "is_enabled": True})
        self._emit(EventType.CAPABILITY_ACTIVATED, {"capability_id": capability_id})
        return True

    def deactivate(self, capability_id: str) -> bool:
        self.update(capability_id, {"is_enabled": False})
        self._emit(EventType.CAPABILITY_DEACTIVATED, {"capability_id": capability_id})
        return True

    def deprecate(self, capability_id: str, reason: str) -> bool:
        self.update(capability_id, {"state": CapabilityState.DEPRECATED.value})
        self._emit(EventType.CAPABILITY_DEPRECATED, {"capability_id": capability_id, "reason": reason})
        return True

    def record_usage(self, capability_id: str) -> None:
        cap = self.get(capability_id)
        self.update(capability_id, {"use_count": cap.use_count + 1, "last_used_at": datetime.now(timezone.utc)})

    def record_error(self, capability_id: str, error: str) -> None:
        cap = self.get(capability_id)
        self.update(capability_id, {"error_count": cap.error_count + 1})

    def update_performance_profile(self, capability_id: str, profile: PerformanceProfile) -> None:
        self.update(capability_id, {"performance_profile": profile})

    def update_health_status(self, capability_id: str, status: HealthStatus) -> None:
        self.update(capability_id, {"health_status": status.value, "last_health_check": datetime.now(timezone.utc)})

    def find_alternatives(self, capability_id: str) -> list[Capability]:
        cap = self.get(capability_id)
        return [c for c in self.get_all() if c.capability_id != cap.capability_id and c.capability_type == cap.capability_type and c.category == cap.category]

    def find_best(self, capability_type: CapabilityType, category: str, optimize_for: str = "latency") -> Capability | None:
        candidates = [c for c in self.get_all() if c.capability_type == capability_type and c.category == category and c.is_enabled]
        if not candidates:
            return None
        if optimize_for == "latency":
            return min(candidates, key=lambda c: c.performance_profile.avg_latency_ms or float("inf"))
        if optimize_for == "reliability":
            return max(candidates, key=lambda c: c.performance_profile.reliability)
        return max(candidates, key=lambda c: c.priority_weight)

    def export_registry(self) -> dict:
        payload = {"capabilities": [c.to_dict() for c in self.get_all()]}
        self._emit(EventType.REGISTRY_EXPORTED, {"count": len(payload["capabilities"])})
        return payload

    def import_registry(self, data: dict) -> int:
        imported = 0
        for item in data.get("capabilities", []):
            self.register(Capability.from_dict(item))
            imported += 1
        self._emit(EventType.REGISTRY_IMPORTED, {"count": imported})
        return imported
