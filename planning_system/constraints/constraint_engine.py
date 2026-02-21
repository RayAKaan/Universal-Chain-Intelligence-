from __future__ import annotations

from dataclasses import dataclass, field

from planning_system.constraints.resource_constraints import MaxCPUConstraint, MaxMemoryConstraint
from planning_system.constraints.time_constraints import MaxDurationConstraint


@dataclass
class ConstraintResult:
    constraint: object
    satisfied: bool
    actual_value: object
    margin: float


@dataclass
class ConstraintReport:
    all_satisfied: bool
    hard_satisfied: bool
    soft_satisfied: bool
    results: list[ConstraintResult] = field(default_factory=list)


class ConstraintViolationError(Exception):
    pass


class ConstraintEngine:
    def evaluate(self, plan, constraints):
        results = []
        for c in constraints:
            sat, actual = self.check_constraint(plan, c)
            margin = 0.0
            if isinstance(actual, (int, float)) and isinstance(c.value, (int, float)):
                margin = c.value - actual
            results.append(ConstraintResult(c, sat, actual, margin))
        all_sat = all(r.satisfied for r in results)
        hard_sat = all(r.satisfied for r in results if r.constraint.is_hard)
        soft_sat = all(r.satisfied for r in results if not r.constraint.is_hard)
        return ConstraintReport(all_sat, hard_sat, soft_sat, results)

    def enforce(self, plan, constraints):
        report = self.evaluate(plan, constraints)
        if not report.hard_satisfied:
            plan.parallelism_degree = max(1, plan.parallelism_degree - 1)
        return plan

    def check_constraint(self, plan, constraint):
        p = constraint.parameter.lower()
        if p in {"cpu", "max_cpu"}:
            return MaxCPUConstraint(plan, constraint.value)
        if p in {"memory", "ram"}:
            return MaxMemoryConstraint(plan, constraint.value)
        if p in {"duration", "time"}:
            return MaxDurationConstraint(plan, constraint.value)
        if hasattr(constraint, "_fn"):
            return constraint._fn(plan)
        return True, None
