"""Demo entrypoint for deterministic execution core."""

from __future__ import annotations

import asyncio
import time
from pathlib import Path

from execution_core.config import DEFAULT_CONFIG
from execution_core.core.execution_engine import (
    APITaskHandler,
    ExecutionEngine,
    ExternalScriptHandler,
    PythonFunctionHandler,
    ShellCommandHandler,
)
from execution_core.core.scheduler import Scheduler
from execution_core.core.task import Task
from execution_core.monitoring.execution_logger import build_logger
from execution_core.monitoring.execution_monitor import ExecutionMonitor
from execution_core.resource.resource_manager import ResourceManager


def multiply(a: int, b: int) -> int:
    return a * b


async def run_demo() -> None:
    logger = build_logger("execution_core.main")
    monitor = ExecutionMonitor()
    resource_manager = ResourceManager(max_threads=DEFAULT_CONFIG.max_workers)
    engine = ExecutionEngine(DEFAULT_CONFIG, monitor, resource_manager)

    engine.register_handler("PythonFunctionTask", PythonFunctionHandler())
    engine.register_handler("ShellCommandTask", ShellCommandHandler())
    engine.register_handler("ExternalScriptTask", ExternalScriptHandler())
    engine.register_handler("APITask", APITaskHandler())

    scheduler = Scheduler(engine, DEFAULT_CONFIG)
    scheduler.start()

    python_task = Task(
        task_type="PythonFunctionTask",
        priority=1,
        payload={"function": multiply, "args": [6, 7]},
    )

    shell_task = Task(
        task_type="ShellCommandTask",
        priority=2,
        payload={"command": "echo deterministic-shell-task"},
    )

    script_path = Path(__file__).with_name("demo_script.sh")
    script_path.write_text("#!/usr/bin/env bash\necho external-script-ran\n", encoding="utf-8")
    script_path.chmod(0o755)

    script_task = Task(
        task_type="ExternalScriptTask",
        priority=3,
        payload={"script_path": str(script_path)},
    )

    for task in (python_task, shell_task, script_task):
        scheduler.submit(task)

    async_task = Task(
        task_type="PythonFunctionTask",
        priority=0,
        payload={"function": sum, "args": [[1, 2, 3, 4]]},
    )
    async_result = await engine.execute_task_async(async_task)
    logger.info("Async task result: %s", async_result.result)

    collected = []
    while len(collected) < 3:
        collected.extend(scheduler.get_completed_tasks())
        await asyncio.sleep(0.05)

    scheduler.stop(wait=True)
    await engine.shutdown()

    for task in sorted(collected + [async_result], key=lambda item: item.priority):
        logger.info("Task %s | type=%s | status=%s | result=%s | error=%s", task.task_id, task.task_type, task.status, task.result, task.error)

    logger.info("Resource snapshot: %s", resource_manager.get_available_resources())
    logger.info("Execution metrics: %s", monitor.snapshot())

    try:
        script_path.unlink(missing_ok=True)
    except OSError:
        pass


if __name__ == "__main__":
    started = time.time()
    asyncio.run(run_demo())
    build_logger("execution_core.main").info("Demo completed in %.3fs", time.time() - started)
