from __future__ import annotations

import os
import platform
from datetime import datetime, timezone
from uuid import uuid4

from planning_system.models.context import Context


class ContextManager:
    def __init__(self, phase1_adapter):
        self.phase1_adapter = phase1_adapter

    def create_context(self, goal):
        summary = self.phase1_adapter.get_capability_summary()
        return Context(
            context_id=str(uuid4()),
            goal_id=goal.goal_id,
            environment={
                "os": platform.platform(),
                "python_version": platform.python_version(),
                "available_memory_mb": 8192,
                "available_cpu_cores": os.cpu_count() or 1,
                "gpu_available": False,
                "network_available": True,
            },
            available_capabilities=[c.capability_id for c in self.phase1_adapter.get_all_active_capabilities()],
            capability_summary=summary,
            active_constraints=[],
            working_directory=os.getcwd(),
            temp_directory="/tmp",
        )

    def update_context(self, context, updates):
        context.variables.update(updates)
        context.updated_at = datetime.now(timezone.utc)
        return context

    def set_variable(self, context, key, value):
        context.variables[key] = value

    def get_variable(self, context, key):
        return context.variables.get(key)

    def get_step_output(self, context, step_id, output_key):
        return context.variables.get(f"step:{step_id}:{output_key}")

    def store_step_output(self, context, step_id, outputs):
        for k, v in outputs.items():
            context.variables[f"step:{step_id}:{k}"] = v

    def snapshot(self, context):
        return {
            "context_id": context.context_id,
            "goal_id": context.goal_id,
            "plan_id": context.plan_id,
            "environment": context.environment,
            "available_capabilities": context.available_capabilities,
            "capability_summary": context.capability_summary,
            "variables": context.variables,
        }

    def restore(self, snapshot):
        return Context(context_id=snapshot["context_id"], goal_id=snapshot["goal_id"], plan_id=snapshot.get("plan_id"), environment=snapshot.get("environment", {}), available_capabilities=snapshot.get("available_capabilities", []), capability_summary=snapshot.get("capability_summary", {}), variables=snapshot.get("variables", {}))
