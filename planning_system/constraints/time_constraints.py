from __future__ import annotations


def MaxDurationConstraint(plan, value):
    return plan.total_estimated_duration_ms <= value, plan.total_estimated_duration_ms


def DeadlineConstraint(plan, deadline):
    return True, 0


def MaxStepDurationConstraint(plan, value):
    mx = max((s.estimated_duration_ms for s in plan.steps), default=0)
    return mx <= value, mx
