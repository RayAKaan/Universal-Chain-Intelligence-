from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class GoalType(str, Enum):
    BUILD = "BUILD"
    TRANSFORM = "TRANSFORM"
    ANALYZE = "ANALYZE"
    DEPLOY = "DEPLOY"
    OPTIMIZE = "OPTIMIZE"
    FIX = "FIX"
    MONITOR = "MONITOR"
    AUTOMATE = "AUTOMATE"
    QUERY = "QUERY"
    COMPOSITE = "COMPOSITE"


class Priority(int, Enum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    BACKGROUND = 4


class GoalStatus(str, Enum):
    PENDING = "PENDING"
    INTERPRETING = "INTERPRETING"
    PLANNING = "PLANNING"
    PLANNED = "PLANNED"
    VALIDATING = "VALIDATING"
    VALIDATED = "VALIDATED"
    EXECUTING = "EXECUTING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    PARTIALLY_COMPLETED = "PARTIALLY_COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REPLANNING = "REPLANNING"


@dataclass
class Intent:
    action: str
    target: str
    domain: str
    qualifiers: list[str] = field(default_factory=list)


@dataclass
class GoalInput:
    name: str
    type: str
    description: str
    required: bool
    value: Any = None
    source: str = ""


@dataclass
class GoalOutput:
    name: str
    type: str
    description: str
    success_criteria: str


@dataclass
class GoalConstraint:
    constraint_type: str
    parameter: str
    operator: str
    value: Any
    unit: str
    is_hard: bool = True


@dataclass
class Goal:
    goal_id: str = field(default_factory=lambda: str(uuid4()))
    raw_input: str = ""
    title: str = ""
    description: str = ""
    goal_type: GoalType = GoalType.COMPOSITE
    priority: Priority = Priority.MEDIUM
    intent: Intent = field(default_factory=lambda: Intent(action="", target="", domain="system", qualifiers=[]))
    inputs: list[GoalInput] = field(default_factory=list)
    outputs: list[GoalOutput] = field(default_factory=list)
    constraints: list[GoalConstraint] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    parent_goal_id: str | None = None
    sub_goal_ids: list[str] = field(default_factory=list)
    status: GoalStatus = GoalStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    deadline: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["goal_type"] = self.goal_type.value
        data["priority"] = int(self.priority.value)
        data["status"] = self.status.value
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        data["deadline"] = self.deadline.isoformat() if self.deadline else None
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Goal":
        d = dict(data)
        d["goal_type"] = GoalType(d.get("goal_type", GoalType.COMPOSITE.value))
        d["priority"] = Priority(d.get("priority", Priority.MEDIUM.value))
        d["status"] = GoalStatus(d.get("status", GoalStatus.PENDING.value))
        d["intent"] = Intent(**d.get("intent", {"action": "", "target": "", "domain": "system", "qualifiers": []}))
        d["inputs"] = [GoalInput(**x) for x in d.get("inputs", [])]
        d["outputs"] = [GoalOutput(**x) for x in d.get("outputs", [])]
        d["constraints"] = [GoalConstraint(**x) for x in d.get("constraints", [])]
        for k in ("created_at", "updated_at", "deadline"):
            if isinstance(d.get(k), str):
                d[k] = datetime.fromisoformat(d[k])
        return cls(**d)
