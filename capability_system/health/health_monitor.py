from __future__ import annotations

import logging
import threading
import time

from capability_system.events.event_types import Event, EventType
from capability_system.health.health_checks import (
    check_api_capability,
    check_model_capability,
    check_plugin_capability,
    check_python_capability,
    check_shell_capability,
)
from capability_system.models.capability import CapabilityState, CapabilityType, HealthStatus


class HealthMonitor:
    def __init__(self, registry, lifecycle_manager, event_bus, degraded_threshold: int = 3, failed_threshold: int = 10):
        self.logger = logging.getLogger("capability_system.health")
        self.registry = registry
        self.lifecycle_manager = lifecycle_manager
        self.event_bus = event_bus
        self.degraded_threshold = degraded_threshold
        self.failed_threshold = failed_threshold
        self.failures: dict[str, int] = {}
        self._thread = None
        self._stop = threading.Event()

    def start(self, interval_seconds: int = 60) -> None:
        if self._thread and self._thread.is_alive():
            return

        def loop():
            while not self._stop.is_set():
                self.check_all()
                time.sleep(interval_seconds)

        self._stop.clear()
        self._thread = threading.Thread(target=loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)

    def check_health(self, capability_id: str) -> HealthStatus:
        cap = self.registry.get(capability_id)
        if cap.capability_type in {CapabilityType.PYTHON_FUNCTION, CapabilityType.PYTHON_CLASS}:
            status = check_python_capability(cap)
        elif cap.capability_type in {CapabilityType.SHELL_COMMAND, CapabilityType.SYSTEM_BINARY, CapabilityType.EXTERNAL_SCRIPT}:
            status = check_shell_capability(cap)
        elif cap.capability_type == CapabilityType.REST_API:
            status = check_api_capability(cap)
        elif cap.capability_type == CapabilityType.MODEL_INFERENCE:
            status = check_model_capability(cap)
        elif cap.capability_type == CapabilityType.PLUGIN:
            status = check_plugin_capability(cap)
        else:
            status = HealthStatus.UNKNOWN

        previous = cap.health_status
        self.registry.update_health_status(capability_id, status)
        if status in {HealthStatus.UNHEALTHY, HealthStatus.DEGRADED}:
            self.failures[capability_id] = self.failures.get(capability_id, 0) + 1
        else:
            self.failures[capability_id] = 0

        if self.failures[capability_id] >= self.failed_threshold:
            self.lifecycle_manager.transition(capability_id, CapabilityState.FAILED, "health threshold reached")
        elif self.failures[capability_id] >= self.degraded_threshold:
            self.lifecycle_manager.transition(capability_id, CapabilityState.DEGRADED, "health degradation detected")

        if previous != status:
            self.event_bus.publish(Event(EventType.CAPABILITY_HEALTH_CHANGED, "health_monitor", {"capability_id": capability_id, "from": previous.value, "to": status.value}))
        return status

    def check_all(self) -> dict[str, HealthStatus]:
        result = {}
        for cap in self.registry.get_active():
            result[cap.capability_id] = self.check_health(cap.capability_id)
        return result

    def get_unhealthy(self):
        return [c for c in self.registry.get_all() if c.health_status == HealthStatus.UNHEALTHY]

    def get_degraded(self):
        return [c for c in self.registry.get_all() if c.health_status == HealthStatus.DEGRADED]
