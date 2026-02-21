from __future__ import annotations

from execution_core.core.task import Task


class Phase0Adapter:
    def __init__(self, execution_engine, scheduler, resource_manager):
        self.execution_engine = execution_engine
        self.scheduler = scheduler
        self.resource_manager = resource_manager
        self._tasks = {}

    def submit_step(self, step, payload):
        task_type = {
            "python_function": "PythonFunctionTask",
            "shell_command": "ShellCommandTask",
            "api_call": "APITask",
            "script": "ExternalScriptTask",
        }.get(step.execution_type, "PythonFunctionTask")
        if task_type == "PythonFunctionTask" and "function" not in payload:
            payload["function"] = lambda *a, **k: {"ok": True, "step": step.name}
            payload.setdefault("args", [])
        task = Task(priority=1, task_type=task_type, payload=payload)
        self._tasks[task.task_id] = task
        return self.execution_engine.execute_task(task)

    def execute_step_sync(self, step, payload):
        return self.submit_step(step, payload).result

    def execute_step_async(self, step, payload):
        task_type = {
            "python_function": "PythonFunctionTask",
            "shell_command": "ShellCommandTask",
            "api_call": "APITask",
            "script": "ExternalScriptTask",
        }.get(step.execution_type, "PythonFunctionTask")
        if task_type == "PythonFunctionTask" and "function" not in payload:
            payload["function"] = lambda *a, **k: {"ok": True, "step": step.name}
            payload.setdefault("args", [])
        if task_type == "PythonFunctionTask" and "function" not in payload:
            payload["function"] = lambda *a, **k: {"ok": True, "step": step.name}
            payload.setdefault("args", [])
        task = Task(priority=1, task_type=task_type, payload=payload)
        self._tasks[task.task_id] = task
        return self.execution_engine.execute_task_threaded(task)

    def get_task_status(self, task_id):
        return self._tasks.get(task_id).status if task_id in self._tasks else "unknown"

    def get_available_resources(self):
        return self.resource_manager.get_available_resources()

    def cancel_task(self, task_id):
        return False
