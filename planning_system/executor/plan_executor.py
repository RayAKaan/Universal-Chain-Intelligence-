from __future__ import annotations

import threading
import time

from planning_system.executor.execution_coordinator import ExecutionCoordinator
from planning_system.models.execution_result import ExecutionResult


class PlanExecutionError(Exception):
    pass


class PlanExecutor:
    def __init__(self, phase0_bridge, phase1_bridge, plan_monitor, rollback_manager, config, step_executor, failure_handler):
        self.phase0_bridge = phase0_bridge
        self.phase1_bridge = phase1_bridge
        self.plan_monitor = plan_monitor
        self.rollback_manager = rollback_manager
        self.config = config
        self.step_executor = step_executor
        self.failure_handler = failure_handler
        self._state = {}

    def execute(self, plan, context):
        context.plan_id = plan.plan_id
        self.plan_monitor.start_monitoring(plan)
        plan.status = "EXECUTING"
        start = time.perf_counter()
        coord = ExecutionCoordinator(plan.execution_graph, self.step_executor, self.config, self.plan_monitor, self.failure_handler)
        result = coord.run(context)
        result.plan_id = plan.plan_id
        result.goal_id = plan.goal_id
        result.total_duration_ms = (time.perf_counter() - start) * 1000
        result.status = "success" if result.steps_failed == 0 else "partial_success"
        self.plan_monitor.on_plan_completed(plan, result)
        return result

    def execute_async(self, plan, context):
        eid = f"exec-{plan.plan_id}"
        self._state[eid] = {"status": "RUNNING"}

        def run():
            try:
                self.execute(plan, context)
                self._state[eid]["status"] = "COMPLETED"
            except Exception as exc:
                self._state[eid]["status"] = f"FAILED: {exc}"

        threading.Thread(target=run, daemon=True).start()
        return eid

    def pause(self, plan_id):
        self._state[plan_id] = {"status": "PAUSED"}
        return True

    def resume(self, plan_id):
        self._state[plan_id] = {"status": "RUNNING"}
        return True

    def cancel(self, plan_id):
        self._state[plan_id] = {"status": "CANCELLED"}
        return True

    def get_status(self, plan_id):
        return self._state.get(plan_id, {"status": "UNKNOWN"})
