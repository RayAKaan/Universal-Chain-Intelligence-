from __future__ import annotations

import logging
import threading
import time

from capability_system.events.event_types import Event, EventType
from capability_system.models.discovery_result import DiscoveryResult
from capability_system.utils.hashing import generate_fingerprint


class DiscoveryEngine:
    def __init__(self, registry, event_bus, config_module):
        self.logger = logging.getLogger("capability_system.discovery.engine")
        self.registry = registry
        self.event_bus = event_bus
        self.config = config_module
        self.scanners = {}
        self._thread = None
        self._stop_event = threading.Event()

    def register_scanner(self, scanner) -> None:
        self.scanners[scanner.scanner_name] = scanner

    def unregister_scanner(self, scanner_name: str) -> None:
        self.scanners.pop(scanner_name, None)

    def get_registered_scanners(self) -> list[str]:
        return list(self.scanners.keys())

    def run_scanner(self, scanner_name: str) -> DiscoveryResult:
        scanner = self.scanners[scanner_name]
        return scanner.scan()

    def run_full_scan(self) -> list[DiscoveryResult]:
        self.event_bus.publish(Event(event_type=EventType.DISCOVERY_SCAN_STARTED, source="discovery_engine", data={"scanners": self.get_registered_scanners()}))
        results = []
        for name, scanner in self.scanners.items():
            if not scanner.is_available():
                continue
            try:
                result = scanner.scan()
                for cap in result.capabilities_found[:150]:
                    try:
                        existing = self.registry.get_by_name(cap.name, cap.version)
                        if existing is None:
                            self.registry.register(cap)
                            self.event_bus.publish(Event(event_type=EventType.CAPABILITY_DISCOVERED, source=name, data={"capability_id": cap.capability_id, "name": cap.name}))
                        else:
                            new_fp = generate_fingerprint(cap)
                            if existing.fingerprint != new_fp:
                                self.registry.update(existing.capability_id, {"description": cap.description, "execution_endpoint": cap.execution_endpoint})
                    except Exception:
                        self.logger.exception("Failed to register discovered capability: %s", cap.name)
                results.append(result)
            except Exception:
                self.logger.exception("Scanner failed: %s", name)
        self.event_bus.publish(Event(event_type=EventType.DISCOVERY_SCAN_COMPLETED, source="discovery_engine", data={"result_count": len(results)}))
        return results

    def start_continuous_discovery(self, interval_seconds: int = 300) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()

        def loop():
            while not self._stop_event.is_set():
                self.run_full_scan()
                time.sleep(interval_seconds)

        self._thread = threading.Thread(target=loop, daemon=True, name="discovery-loop")
        self._thread.start()

    def stop_continuous_discovery(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)
