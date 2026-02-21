from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class StepType(str, Enum):
    ATOMIC = "ATOMIC"
    COMPOSITE = "COMPOSITE"
    CONDITIONAL = "CONDITIONAL"
    LOOP = "LOOP"
    PARALLEL_GROUP = "PARALLEL_GROUP"
    CHECKPOINT = "CHECKPOINT"
    GATE = "GATE"
    TRANSFORM = "TRANSFORM"


class StepStatus(str, Enum):
    PENDING = "PENDING"
    BLOCKED = "BLOCKED"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    RETRYING = "RETRYING"
    CANCELLED = "CANCELLED"
    TIMED_OUT = "TIMED_OUT"


class FailureAction(str, Enum):
    RETRY = "RETRY"
    SKIP = "SKIP"
    ABORT_PLAN = "ABORT_PLAN"
    FALLBACK = "FALLBACK"
    REPLAN = "REPLAN"
    CONTINUE_DEGRADED = "CONTINUE_DEGRADED"


@dataclass
class RetryPolicy:
    max_retries: int = 3
    retry_delay_ms: float = 1000
    backoff_multiplier: float = 2.0
    retryable_errors: list[str] = field(default_factory=list)


@dataclass
class StepCondition:
    condition_type: str
    expression: str
    source_step_id: str
    source_output_key: str
    operator: str
    value: object


@dataclass
class PlanStep:
    step_id: str = field(default_factory=lambda: str(uuid4()))
    plan_id: str = ""
    name: str = ""
    description: str = ""
    step_type: StepType = StepType.ATOMIC
    level: int = 0
    parent_step_id: str | None = None
    child_step_ids: list[str] = field(default_factory=list)
    is_leaf: bool = True
    dependencies: list[str] = field(default_factory=list)
    dependents: list[str] = field(default_factory=list)
    capability_id: str | None = None
    capability_name: str = ""
    execution_type: str = ""
    input_mapping: dict = field(default_factory=dict)
    output_keys: list[str] = field(default_factory=lambda: ["result"])
    estimated_duration_ms: float = 1000.0
    estimated_cost: float = 0.0
    resource_requirements: object = None
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    timeout_ms: float = 60000
    conditions: list[StepCondition] = field(default_factory=list)
    on_failure: FailureAction = FailureAction.RETRY
    fallback_step_id: str | None = None
    status: StepStatus = StepStatus.PENDING
    result: object = None
    error: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    retry_count: int = 0
    metadata: dict = field(default_factory=dict)


@dataclass
class StepResult:
    step_id: str
    step_name: str
    status: str
    result: object = None
    error: str | None = None
    duration_ms: float = 0.0
    retry_count: int = 0
    capability_used: str = ""
