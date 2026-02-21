from __future__ import annotations

import logging
from datetime import datetime, timezone

from capability_system.events.event_types import Event, EventType
from capability_system.lifecycle.capability_states import VALID_TRANSITIONS, is_valid_transition
from capability_system.models.capability import CapabilityState


class LifecycleManager:
    def __init__(self, registry, database, event_bus):
        self.logger = logging.getLogger("capability_system.lifecycle")
        self.registry = registry
        self.db = database
        self.event_bus = event_bus

    def transition(self, capability_id: str, target_state: CapabilityState, reason: str = "") -> bool:
        cap = self.registry.get(capability_id)
        if not is_valid_transition(cap.state, target_state):
            return False
        from_state = cap.state
        self.registry.update(capability_id, {"state": target_state.value})
        self.db.execute("INSERT INTO state_transitions(capability_id,from_state,to_state,reason,timestamp) VALUES (?,?,?,?,?)", (capability_id, from_state.value, target_state.value, reason, datetime.now(timezone.utc).isoformat()))
        self.event_bus.publish(Event(EventType.CAPABILITY_STATE_CHANGED, "lifecycle_manager", {"capability_id": capability_id, "from": from_state.value, "to": target_state.value, "reason": reason}))
        return True

    def get_transition_history(self, capability_id: str) -> list[dict]:
        rows = self.db.query("SELECT * FROM state_transitions WHERE capability_id = ? ORDER BY id", (capability_id,))
        return [dict(r) for r in rows]

    def get_valid_transitions(self, current_state: CapabilityState) -> list[CapabilityState]:
        return list(VALID_TRANSITIONS.get(current_state, set()))
