from __future__ import annotations

from capability_system.models.capability import CapabilityState

VALID_TRANSITIONS = {
    CapabilityState.DISCOVERED: {CapabilityState.REGISTERING, CapabilityState.REMOVED},
    CapabilityState.REGISTERING: {CapabilityState.REGISTERED, CapabilityState.FAILED, CapabilityState.REMOVED},
    CapabilityState.REGISTERED: {CapabilityState.BENCHMARKING, CapabilityState.ACTIVE, CapabilityState.REMOVED},
    CapabilityState.BENCHMARKING: {CapabilityState.BENCHMARKED, CapabilityState.FAILED, CapabilityState.REMOVED},
    CapabilityState.BENCHMARKED: {CapabilityState.ACTIVE, CapabilityState.REMOVED},
    CapabilityState.ACTIVE: {CapabilityState.DEGRADED, CapabilityState.DEPRECATED, CapabilityState.FAILED, CapabilityState.REMOVED},
    CapabilityState.DEGRADED: {CapabilityState.ACTIVE, CapabilityState.FAILED, CapabilityState.REMOVED},
    CapabilityState.DEPRECATED: {CapabilityState.REMOVED},
    CapabilityState.FAILED: {CapabilityState.REGISTERED, CapabilityState.REMOVED},
    CapabilityState.REMOVED: set(),
}


def is_valid_transition(current_state: CapabilityState, target_state: CapabilityState) -> bool:
    if target_state == CapabilityState.REMOVED:
        return True
    return target_state in VALID_TRANSITIONS.get(current_state, set())
