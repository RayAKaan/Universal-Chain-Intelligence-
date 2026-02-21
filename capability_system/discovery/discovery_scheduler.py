from __future__ import annotations

import logging
import threading
import time


class DiscoveryScheduler:
    def __init__(self, discovery_engine):
        self.logger = logging.getLogger("capability_system.discovery.scheduler")
        self.discovery_engine = discovery_engine
        self._schedules = {}
        self._failures = {}
        self._thread = None
        self._stop = threading.Event()

    def set_schedule(self, scanner_name: str, interval_seconds: int) -> None:
        self._schedules[scanner_name] = interval_seconds

    def trigger_scan(self, scanner_name: str):
        return self.discovery_engine.run_scanner(scanner_name)

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        def loop():
            last = {k: 0.0 for k in self._schedules}
            while not self._stop.is_set():
                now = time.time()
                for scanner, interval in self._schedules.items():
                    if now - last.get(scanner, 0.0) >= interval:
                        try:
                            self.discovery_engine.run_scanner(scanner)
                            last[scanner] = now
                            self._failures[scanner] = 0
                        except Exception:
                            self.logger.exception("Scheduled scan failed: %s", scanner)
                            self._failures[scanner] = self._failures.get(scanner, 0) + 1
                            last[scanner] = now + min(300, 2 ** self._failures[scanner])
                time.sleep(1)

        self._stop.clear()
        self._thread = threading.Thread(target=loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)
