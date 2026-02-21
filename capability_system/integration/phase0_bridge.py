from __future__ import annotations

from capability_system.models.capability import ExecutionType
from capability_system.integration.capability_task_adapter import CapabilityExecutionHandler
from execution_core.config import DEFAULT_CONFIG
from execution_core.core.execution_engine import (
    APITaskHandler,
    ExecutionEngine,
    ExternalScriptHandler,
    PythonFunctionHandler,
    ShellCommandHandler,
)
from execution_core.core.task import Task
from execution_core.monitoring.execution_monitor import ExecutionMonitor
from execution_core.resource.resource_manager import ResourceManager


class Phase0Bridge:
    def __init__(self, registry):
        self.registry = registry
        self.engine = ExecutionEngine(DEFAULT_CONFIG, ExecutionMonitor(), ResourceManager(DEFAULT_CONFIG.max_workers))
        self.engine.register_handler("PythonFunctionTask", PythonFunctionHandler())
        self.engine.register_handler("ShellCommandTask", ShellCommandHandler())
        self.engine.register_handler("ExternalScriptTask", ExternalScriptHandler())
        self.engine.register_handler("APITask", APITaskHandler())

    def create_task_from_capability(self, capability, payload: dict) -> Task:
        mapping = {
            ExecutionType.PYTHON_FUNCTION: "PythonFunctionTask",
            ExecutionType.SHELL_COMMAND: "ShellCommandTask",
            ExecutionType.API_CALL: "APITask",
            ExecutionType.SCRIPT: "ExternalScriptTask",
            ExecutionType.MODEL_INFERENCE: "PythonFunctionTask",
            ExecutionType.PLUGIN: "PythonFunctionTask",
        }
        task_type = mapping.get(capability.execution_type, "CapabilityTask")
        merged = dict(capability.execution_config)
        merged.update(payload)
        if task_type == "PythonFunctionTask" and "function" not in merged:
            import importlib

            module_name, fn_name = capability.execution_endpoint.rsplit(".", 1)
            merged["function"] = getattr(importlib.import_module(module_name), fn_name)
        if task_type == "ShellCommandTask" and "command" not in merged:
            merged["command"] = capability.execution_endpoint
        if task_type == "ExternalScriptTask" and "script_path" not in merged:
            merged["script_path"] = capability.execution_endpoint
        if task_type == "APITask" and "url" not in merged:
            merged["url"] = capability.execution_endpoint
        if task_type == "PythonFunctionTask" and "function" not in merged:
            merged["function"] = lambda *a, **k: {"endpoint": capability.execution_endpoint, "input": payload}
        return Task(priority=1, task_type=task_type, payload=merged)

    def execute_capability(self, capability_id: str, payload: dict):
        cap = self.registry.get(capability_id)
        task = self.create_task_from_capability(cap, payload)
        result = self.engine.execute_task(task)
        if result.status == "completed":
            self.registry.record_usage(capability_id)
            return result.result
        self.registry.record_error(capability_id, result.error or "unknown")
        raise RuntimeError(result.error)

    def get_execution_handler_for_capability(self, capability):
        return CapabilityExecutionHandler(capability)
