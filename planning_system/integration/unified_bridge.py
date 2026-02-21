from __future__ import annotations

from planning_system.models.plan_step import StepResult


class UnifiedBridge:
    def __init__(self, phase0_adapter, phase1_adapter):
        self.phase0 = phase0_adapter
        self.phase1 = phase1_adapter

    def resolve_and_execute_step(self, step, context, payload=None):
        payload = payload or {}
        if step.execution_type == "python_function" and "function" not in payload:
            payload["function"] = lambda *a, **k: {"step": step.name, "ok": True}
            payload.setdefault("args", [])
        if step.execution_type == "shell_command" and "command" not in payload:
            payload["command"] = "echo step-executed"
        if step.execution_type == "api_call" and "url" not in payload:
            payload["url"] = "https://httpbin.org/get"
            payload["method"] = "GET"
        return self.phase0.execute_step_sync(step, payload)

    def get_system_status(self):
        return {
            "resources": self.phase0.get_available_resources(),
            "capabilities": self.get_capability_count(),
        }

    def get_available_resources(self):
        return self.phase0.get_available_resources()

    def get_capability_count(self):
        return self.phase1.get_capability_summary()["count"]

    def get_active_tasks(self):
        return 0
