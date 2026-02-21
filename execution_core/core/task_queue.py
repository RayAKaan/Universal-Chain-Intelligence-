"""Priority queue wrapper for tasks."""

from __future__ import annotations

import queue
from typing import Optional

from execution_core.core.task import Task


class TaskQueue:
    def __init__(self, maxsize: int = 0) -> None:
        self._queue: queue.PriorityQueue[Task] = queue.PriorityQueue(maxsize=maxsize)

    def put(self, task: Task) -> None:
        self._queue.put(task)

    def get(self, timeout: Optional[float] = None) -> Task:
        return self._queue.get(timeout=timeout)

    def task_done(self) -> None:
        self._queue.task_done()

    def qsize(self) -> int:
        return self._queue.qsize()

    def empty(self) -> bool:
        return self._queue.empty()
