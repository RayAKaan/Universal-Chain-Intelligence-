from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class ConstraintType(str, Enum):
    RESOURCE = "RESOURCE"
    TIME = "TIME"
    COST = "COST"
    QUALITY = "QUALITY"
    DEPENDENCY = "DEPENDENCY"
    CUSTOM = "CUSTOM"


@dataclass
class Constraint:
    constraint_id: str = field(default_factory=lambda: str(uuid4()))
    constraint_type: ConstraintType = ConstraintType.CUSTOM
    name: str = ""
    description: str = ""
    parameter: str = ""
    operator: str = "eq"
    value: object = None
    unit: str = ""
    is_hard: bool = True
    priority: int = 1
    source: str = "goal"
