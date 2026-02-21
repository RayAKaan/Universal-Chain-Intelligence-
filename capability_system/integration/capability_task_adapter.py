from __future__ import annotations

from capability_system.models.capability import ExecutionType
from execution_core.interfaces.execution_interface import ExecutionInterface


class CapabilityExecutionHandler(ExecutionInterface):
    def __init__(self, capability):
        self.capability = capability

    def execute(self, task_payload):
        endpoint = self.capability.execution_endpoint
        execution_type = self.capability.execution_type
        if execution_type == ExecutionType.PYTHON_FUNCTION:
            fn = task_payload["function"]
            return fn(*task_payload.get("args", []), **task_payload.get("kwargs", {}))
        if execution_type == ExecutionType.SHELL_COMMAND:
            import subprocess

            out = subprocess.run(task_payload["command"], shell=True, text=True, capture_output=True, check=False)
            if out.returncode != 0:
                raise RuntimeError(out.stderr)
            return out.stdout.strip()
        if execution_type == ExecutionType.API_CALL:
            import urllib.request

            with urllib.request.urlopen(task_payload["url"], timeout=10) as response:
                return response.read().decode("utf-8")
        if execution_type == ExecutionType.SCRIPT:
            import subprocess

            out = subprocess.run([endpoint], text=True, capture_output=True, check=False)
            if out.returncode != 0:
                raise RuntimeError(out.stderr)
            return out.stdout.strip()
        if execution_type in {ExecutionType.MODEL_INFERENCE, ExecutionType.PLUGIN}:
            return {"endpoint": endpoint, "input": task_payload.get("input")}
        raise ValueError(f"Unsupported execution type: {execution_type}")

    def validate(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("Payload must be dict")

    def get_requirements(self):
        rr = self.capability.resource_requirements
        return {"threads": max(1, int(rr.min_cpu_cores))}
