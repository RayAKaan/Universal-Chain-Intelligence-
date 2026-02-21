"""Resource allocation and bookkeeping."""

from __future__ import annotations

import threading
from typing import Any, Dict

from execution_core.core.task import Task
from execution_core.resource.resource_monitor import ResourceMonitor


class ResourceManager:
    def __init__(self, max_threads: int) -> None:
        self._max_threads = max_threads
        self._available_threads = max_threads
        self._monitor = ResourceMonitor()
        self._lock = threading.Lock()

    def get_available_resources(self) -> Dict[str, Any]:
        sample = self._monitor.sample()
        with self._lock:
            threads = self._available_threads
        sample.update(
            {
                "available_threads": threads,
                "max_threads": self._max_threads,
                "gpu_available": False,
            }
        )
        return sample

    def allocate_resources(self, task: Task) -> bool:
        requirements = task.payload.get("requirements", {})
        needed_threads = max(1, int(requirements.get("threads", 1)))
        with self._lock:
            if needed_threads <= self._available_threads:
                self._available_threads -= needed_threads
                task.payload.setdefault("_allocated", {})["threads"] = needed_threads
                return True
        return False

    def release_resources(self, task: Task) -> None:
        allocated = task.payload.get("_allocated", {})
        used_threads = int(allocated.get("threads", 0))
        if used_threads <= 0:
            return
        with self._lock:
            self._available_threads = min(self._max_threads, self._available_threads + used_threads)
        allocated.pop("threads", None)
