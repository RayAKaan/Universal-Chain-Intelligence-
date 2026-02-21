from __future__ import annotations

import time
from dataclasses import dataclass

from planning_system.monitor.progress_tracker import ProgressTracker


@dataclass
class ProgressReport:
    plan_id: str
    total_steps: int
    completed: int
    failed: int
    running: int
    pending: int
    skipped: int
    percent_complete: float
    estimated_remaining_ms: float
    current_step_names: list[str]
    elapsed_ms: float


class PlanMonitor:
    def __init__(self, event_bus, config):
        self.event_bus = event_bus
        self.config = config
        self.tracker = ProgressTracker()
        self.started = {}
        self.plan_lookup = {}

    def start_monitoring(self, plan):
        self.started[plan.plan_id] = time.time()
        self.plan_lookup[plan.plan_id] = plan

    def stop_monitoring(self, plan_id):
        self.started.pop(plan_id, None)

    def get_progress(self, plan_id):
        plan = self.plan_lookup[plan_id]
        total = len(plan.steps)
        completed = len([s for s in plan.steps if s.status == "COMPLETED"])
        failed = len([s for s in plan.steps if s.status == "FAILED"])
        running = len([s for s in plan.steps if s.status == "RUNNING"])
        pending = len([s for s in plan.steps if s.status == "PENDING"])
        skipped = len([s for s in plan.steps if s.status == "SKIPPED"])
        elapsed = (time.time() - self.started.get(plan_id, time.time())) * 1000
        return ProgressReport(plan_id, total, completed, failed, running, pending, skipped, (completed / total * 100 if total else 0), self.tracker.estimate_remaining(plan_id), [s.name for s in plan.steps if s.status == "RUNNING"], elapsed)

    def get_timeline(self, plan_id):
        return self.tracker.get_step_history(plan_id)

    def on_step_started(self, step):
        self.tracker.track(step.plan_id, step.step_id, "RUNNING")

    def on_step_completed(self, step, result):
        self.tracker.track(step.plan_id, step.step_id, "COMPLETED", result)

    def on_step_failed(self, step, error):
        self.tracker.track(step.plan_id, step.step_id, "FAILED", error)

    def on_plan_completed(self, plan, result):
        self.tracker.track(plan.plan_id, "plan", "PLAN_COMPLETED", result.status)

    def on_plan_failed(self, plan, error):
        self.tracker.track(plan.plan_id, "plan", "PLAN_FAILED", error)
