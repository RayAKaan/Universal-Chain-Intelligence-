from __future__ import annotations

from planning_system.models.plan_step import FailureAction


class FailureHandler:
    def handle_failure(self, step, error, plan, context):
        if self.should_retry(step):
            return FailureAction.RETRY
        if step.fallback_step_id:
            return FailureAction.FALLBACK
        if self.should_replan(plan, step):
            return FailureAction.REPLAN
        return FailureAction.ABORT_PLAN

    def should_retry(self, step):
        return step.retry_count < step.retry_policy.max_retries

    def get_fallback(self, step, plan):
        return next((s for s in plan.steps if s.step_id == step.fallback_step_id), None)

    def should_replan(self, plan, failed_step):
        completed = len([s for s in plan.steps if s.status == "COMPLETED"])
        return completed >= max(1, len(plan.steps) // 3)
