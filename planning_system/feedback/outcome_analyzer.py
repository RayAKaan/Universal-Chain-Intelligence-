from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class OutcomeAnalysis:
    success: bool
    bottleneck_steps: list[str] = field(default_factory=list)
    failure_points: list[str] = field(default_factory=list)
    underperforming_capabilities: list[str] = field(default_factory=list)
    resource_efficiency: float = 1.0
    time_efficiency: float = 1.0
    suggestions: list[str] = field(default_factory=list)


def analyze(result):
    fails = [s.step_id for s in result.step_results if s.status != "COMPLETED"]
    bottleneck = sorted(result.step_results, key=lambda s: s.duration_ms, reverse=True)[:2]
    return OutcomeAnalysis(
        success=result.status == "success",
        bottleneck_steps=[b.step_id for b in bottleneck],
        failure_points=fails,
        time_efficiency=1.0,
        suggestions=["Use parallel strategy" if len(fails) > 0 else "Keep strategy"],
    )
