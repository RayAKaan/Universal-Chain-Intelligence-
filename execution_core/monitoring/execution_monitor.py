"""Execution metrics and telemetry."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Dict


@dataclass
class TaskTiming:
    started_at_monotonic: float


class ExecutionMonitor:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._timings: Dict[str, TaskTiming] = {}
        self._running_tasks: set[str] = set()
        self._total = 0
        self._success = 0
        self._failed = 0
        self._total_exec_time = 0.0

    def on_task_started(self, task_id: str) -> None:
        with self._lock:
            self._running_tasks.add(task_id)
            self._timings[task_id] = TaskTiming(started_at_monotonic=time.monotonic())

    def on_task_completed(self, task_id: str, success: bool) -> None:
        with self._lock:
            timing = self._timings.pop(task_id, None)
            if timing:
                self._total_exec_time += max(0.0, time.monotonic() - timing.started_at_monotonic)
            self._running_tasks.discard(task_id)
            self._total += 1
            if success:
                self._success += 1
            else:
                self._failed += 1

    def snapshot(self) -> Dict[str, float | int]:
        with self._lock:
            success_rate = (self._success / self._total) if self._total else 0.0
            failure_rate = (self._failed / self._total) if self._total else 0.0
            avg_time = (self._total_exec_time / self._total) if self._total else 0.0
            return {
                "total_tasks": self._total,
                "running_tasks": len(self._running_tasks),
                "success_rate": success_rate,
                "failure_rate": failure_rate,
                "average_execution_time_seconds": avg_time,
            }
