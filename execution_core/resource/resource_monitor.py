"""Live resource probing utilities."""

from __future__ import annotations

import os
from typing import Any, Dict

try:
    import psutil  # type: ignore
except Exception:  # noqa: BLE001
    psutil = None


class ResourceMonitor:
    def sample(self) -> Dict[str, Any]:
        if psutil is not None:
            cpu_percent = psutil.cpu_percent(interval=0.0)
            vm = psutil.virtual_memory()
            logical_cpus = psutil.cpu_count(logical=True) or (os.cpu_count() or 1)
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": vm.percent,
                "memory_available_bytes": vm.available,
                "logical_cpus": logical_cpus,
            }

        logical_cpus = os.cpu_count() or 1
        return {
            "cpu_percent": 0.0,
            "memory_percent": 0.0,
            "memory_available_bytes": 0,
            "logical_cpus": logical_cpus,
        }
