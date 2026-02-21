from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from planning_system.models.plan_step import StepResult


@dataclass
class ExecutionResult:
    result_id: str = field(default_factory=lambda: str(uuid4()))
    plan_id: str = ""
    goal_id: str = ""
    status: str = "failure"
    step_results: list[StepResult] = field(default_factory=list)
    outputs: dict = field(default_factory=dict)
    total_duration_ms: float = 0.0
    steps_completed: int = 0
    steps_failed: int = 0
    steps_skipped: int = 0
    resource_usage: dict = field(default_factory=dict)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None
    feedback: dict = field(default_factory=dict)
