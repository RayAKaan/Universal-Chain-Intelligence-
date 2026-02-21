from __future__ import annotations

import threading
import time
from pathlib import Path

from safety_system.constitutional.constitution import Constitution


class ConstitutionVerifier:
    def __init__(self, hash_file: str):
        self.hash_file = Path(hash_file)
        self.hash_file.parent.mkdir(parents=True, exist_ok=True)
        self._thread: threading.Thread | None = None
        self._running = False

    def store_hash(self, value: str) -> None:
        self.hash_file.write_text(value)

    def get_stored_hash(self) -> str:
        return self.hash_file.read_text().strip() if self.hash_file.exists() else ""

    def verify_on_boot(self) -> bool:
        current = Constitution.get_integrity_hash()
        stored = self.get_stored_hash()
        if not stored:
            self.store_hash(current)
            return True
        return current == stored

    def verify_runtime(self) -> bool:
        stored = self.get_stored_hash()
        return bool(stored) and Constitution.verify_integrity(stored)

    def schedule_periodic_verification(self, interval_seconds: int = 300) -> None:
        if self._running:
            return
        self._running = True

        def _loop() -> None:
            while self._running:
                self.verify_runtime()
                time.sleep(interval_seconds)

        self._thread = threading.Thread(target=_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
