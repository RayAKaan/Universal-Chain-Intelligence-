from __future__ import annotations

from dataclasses import dataclass, field

from planning_system.models.plan_step import PlanStep


@dataclass
class PlanNode:
    node_id: str
    step: PlanStep
    incoming_edges: list[str] = field(default_factory=list)
    outgoing_edges: list[str] = field(default_factory=list)
    in_degree: int = 0
    out_degree: int = 0
    is_ready: bool = False
    is_completed: bool = False
    is_critical_path: bool = False
    earliest_start: float = 0.0
    latest_start: float = 0.0
    slack: float = 0.0
