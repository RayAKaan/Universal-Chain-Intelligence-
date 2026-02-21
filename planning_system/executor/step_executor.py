from __future__ import annotations

import time

from planning_system.models.plan_step import StepResult


class StepExecutionError(Exception):
    pass


class StepExecutor:
    def __init__(self, unified_bridge, context_manager):
        self.bridge = unified_bridge
        self.context_manager = context_manager

    def resolve_inputs(self, step, context):
        payload = {}
        for k, spec in step.input_mapping.items():
            if spec.get("source") == "step":
                payload[k] = self.context_manager.get_step_output(context, spec["step_id"], spec.get("output_key", "result"))
            elif spec.get("source") == "goal":
                payload[k] = context.variables.get(spec.get("input_key"))
            elif spec.get("source") == "literal":
                payload[k] = spec.get("value")
            elif spec.get("source") == "context":
                payload[k] = context.variables.get(spec.get("context_key"))
        return payload

    def execute_step(self, step, context):
        payload = self.resolve_inputs(step, context)
        started = time.perf_counter()
        try:
            result = self.bridge.resolve_and_execute_step(step, context, payload)
            out = {"result": result}
            self.context_manager.store_step_output(context, step.step_id, out)
            return StepResult(step.step_id, step.name, "COMPLETED", result=result, duration_ms=(time.perf_counter()-started)*1000, retry_count=step.retry_count, capability_used=step.capability_name)
        except Exception as exc:
            return StepResult(step.step_id, step.name, "FAILED", error=str(exc), duration_ms=(time.perf_counter()-started)*1000, retry_count=step.retry_count, capability_used=step.capability_name)

    def execute_with_retry(self, step, context):
        delay = step.retry_policy.retry_delay_ms / 1000
        for attempt in range(step.retry_policy.max_retries + 1):
            step.retry_count = attempt
            res = self.execute_step(step, context)
            if res.status == "COMPLETED":
                return res
            time.sleep(delay)
            delay *= step.retry_policy.backoff_multiplier
        return res

    def execute_with_timeout(self, step, context):
        return self.execute_with_retry(step, context)
