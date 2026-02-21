from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from planning_system.models.constraint import Constraint


@dataclass
class Context:
    context_id: str
    goal_id: str
    plan_id: str | None = None
    environment: dict = field(default_factory=dict)
    available_capabilities: list[str] = field(default_factory=list)
    capability_summary: dict = field(default_factory=dict)
    active_constraints: list[Constraint] = field(default_factory=list)
    execution_history: list[dict] = field(default_factory=list)
    variables: dict = field(default_factory=dict)
    working_directory: str = "."
    temp_directory: str = "/tmp"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
