"""Task scheduler for deterministic dispatch."""

from __future__ import annotations

import queue
import threading
from concurrent.futures import Future
from typing import Dict, List, Optional

from execution_core.config import EngineConfig
from execution_core.core.execution_engine import ExecutionEngine
from execution_core.core.task import Task
from execution_core.core.task_queue import TaskQueue
from execution_core.monitoring.execution_logger import build_logger


class Scheduler:
    def __init__(self, engine: ExecutionEngine, config: EngineConfig) -> None:
        self._engine = engine
        self._config = config
        self._queue = TaskQueue(maxsize=config.max_queue_size)
        self._logger = build_logger("execution_core.scheduler")
        self._dispatch_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._futures: Dict[str, Future[Task]] = {}
        self._lock = threading.Lock()

    def submit(self, task: Task) -> None:
        self._queue.put(task)
        self._logger.info("Task submitted: %s", task.task_id)

    def start(self) -> None:
        if self._dispatch_thread and self._dispatch_thread.is_alive():
            return
        self._stop_event.clear()
        self._dispatch_thread = threading.Thread(target=self._dispatch_loop, name="scheduler-dispatch", daemon=True)
        self._dispatch_thread.start()

    def _dispatch_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                task = self._queue.get(timeout=self._config.scheduler_poll_interval)
            except queue.Empty:
                continue
            future = self._engine.execute_task_threaded(task)
            with self._lock:
                self._futures[task.task_id] = future
            self._queue.task_done()

    def stop(self, wait: bool = True) -> None:
        self._stop_event.set()
        if self._dispatch_thread and wait:
            self._dispatch_thread.join()

    def get_completed_tasks(self) -> List[Task]:
        completed: List[Task] = []
        with self._lock:
            done_ids = [task_id for task_id, future in self._futures.items() if future.done()]
            for task_id in done_ids:
                completed.append(self._futures[task_id].result())
                del self._futures[task_id]
        return completed

    def pending_count(self) -> int:
        return self._queue.qsize()
