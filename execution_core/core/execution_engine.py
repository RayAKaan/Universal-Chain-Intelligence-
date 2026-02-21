"""Deterministic execution engine with pluggable handlers."""

from __future__ import annotations

import asyncio
import json
import subprocess
import threading
import urllib.request
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Dict, Optional

from execution_core.config import EngineConfig
from execution_core.core.task import Task
from execution_core.interfaces.execution_interface import ExecutionInterface
from execution_core.monitoring.execution_logger import build_logger
from execution_core.monitoring.execution_monitor import ExecutionMonitor
from execution_core.resource.resource_manager import ResourceManager
from execution_core.utils.async_utils import run_sync_in_thread


class PythonFunctionHandler(ExecutionInterface):
    def execute(self, task_payload: Dict[str, Any]) -> Any:
        fn: Callable[..., Any] = task_payload["function"]
        args = task_payload.get("args", [])
        kwargs = task_payload.get("kwargs", {})
        return fn(*args, **kwargs)

    def validate(self, payload: Dict[str, Any]) -> None:
        if "function" not in payload or not callable(payload["function"]):
            raise ValueError("PythonFunctionTask requires callable 'function'")

    def get_requirements(self) -> Dict[str, Any]:
        return {"threads": 1}


class ShellCommandHandler(ExecutionInterface):
    def execute(self, task_payload: Dict[str, Any]) -> Any:
        command = task_payload["command"]
        completed = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"Command failed ({completed.returncode}): {completed.stderr.strip()}")
        return completed.stdout.strip()

    def validate(self, payload: Dict[str, Any]) -> None:
        if not payload.get("command"):
            raise ValueError("ShellCommandTask requires non-empty 'command'")

    def get_requirements(self) -> Dict[str, Any]:
        return {"threads": 1}


class ExternalScriptHandler(ExecutionInterface):
    def execute(self, task_payload: Dict[str, Any]) -> Any:
        script = task_payload["script_path"]
        args = task_payload.get("args", [])
        completed = subprocess.run([script, *args], capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"Script failed ({completed.returncode}): {completed.stderr.strip()}")
        return completed.stdout.strip()

    def validate(self, payload: Dict[str, Any]) -> None:
        if not payload.get("script_path"):
            raise ValueError("ExternalScriptTask requires 'script_path'")

    def get_requirements(self) -> Dict[str, Any]:
        return {"threads": 1}


class APITaskHandler(ExecutionInterface):
    def execute(self, task_payload: Dict[str, Any]) -> Any:
        url = task_payload["url"]
        method = task_payload.get("method", "GET").upper()
        headers = task_payload.get("headers", {})
        body = task_payload.get("body")
        encoded_body = json.dumps(body).encode("utf-8") if body is not None else None

        req = urllib.request.Request(url=url, method=method, headers=headers, data=encoded_body)
        with urllib.request.urlopen(req, timeout=task_payload.get("timeout", 10)) as response:
            data = response.read().decode("utf-8")
            return {"status": response.status, "body": data}

    def validate(self, payload: Dict[str, Any]) -> None:
        if not payload.get("url"):
            raise ValueError("APITask requires 'url'")

    def get_requirements(self) -> Dict[str, Any]:
        return {"threads": 1}


class ExecutionEngine:
    def __init__(
        self,
        config: EngineConfig,
        monitor: ExecutionMonitor,
        resource_manager: ResourceManager,
    ) -> None:
        self._config = config
        self._monitor = monitor
        self._resource_manager = resource_manager
        self._logger = build_logger("execution_core.engine")
        self._handlers: Dict[str, ExecutionInterface] = {}
        self._lock = threading.Lock()
        self._thread_pool = ThreadPoolExecutor(
            max_workers=config.max_workers,
            thread_name_prefix=config.thread_name_prefix,
        )

    def register_handler(self, task_type: str, handler: ExecutionInterface) -> None:
        with self._lock:
            self._handlers[task_type] = handler

    def get_handler(self, task_type: str) -> ExecutionInterface:
        with self._lock:
            handler = self._handlers.get(task_type)
        if handler is None:
            raise ValueError(f"No handler registered for task type: {task_type}")
        return handler

    def execute_task(self, task: Task) -> Task:
        handler = self.get_handler(task.task_type)
        try:
            handler.validate(task.payload)
            task.payload.setdefault("requirements", handler.get_requirements())

            if not self._resource_manager.allocate_resources(task):
                raise RuntimeError("Insufficient resources for task execution")

            task.mark_running()
            self._monitor.on_task_started(task.task_id)
            self._logger.info("Task %s started [%s]", task.task_id, task.task_type)
            result = handler.execute(task.payload)
            task.mark_completed(result)
            self._monitor.on_task_completed(task.task_id, success=True)
            self._logger.info("Task %s completed", task.task_id)
        except Exception as exc:  # noqa: BLE001
            task.mark_failed(exc)
            self._monitor.on_task_completed(task.task_id, success=False)
            self._logger.exception("Task %s failed", task.task_id)
        finally:
            self._resource_manager.release_resources(task)
        return task

    async def execute_task_async(self, task: Task) -> Task:
        return await run_sync_in_thread(self.execute_task, task)

    def execute_task_threaded(self, task: Task) -> Future[Task]:
        return self._thread_pool.submit(self.execute_task, task)

    async def shutdown(self) -> None:
        await asyncio.get_running_loop().run_in_executor(None, self._thread_pool.shutdown, True)
