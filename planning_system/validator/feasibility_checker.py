from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FeasibilityReport:
    is_feasible: bool
    feasibility_score: float
    resource_feasible: bool
    time_feasible: bool
    capability_feasible: bool
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


def check_feasibility(plan, context):
    issues = []
    cap_ok = all(s.capability_id for s in plan.steps if s.is_leaf)
    if not cap_ok:
        issues.append("some steps unresolved")
    resource_ok = True
    time_ok = True
    if plan.total_estimated_duration_ms > 3_600_000:
        time_ok = False
        issues.append("plan duration too high")
    score = 1.0 - min(1.0, len(issues) * 0.2)
    return FeasibilityReport(not issues, score, resource_ok, time_ok, cap_ok, issues, ["reduce complexity" if issues else ""])
