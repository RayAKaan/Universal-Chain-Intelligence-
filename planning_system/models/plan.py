from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from planning_system.models.plan_step import PlanStep


class PlanStatus(str, Enum):
    DRAFT = "DRAFT"
    OPTIMIZING = "OPTIMIZING"
    OPTIMIZED = "OPTIMIZED"
    VALIDATING = "VALIDATING"
    VALIDATED = "VALIDATED"
    READY = "READY"
    EXECUTING = "EXECUTING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    PARTIALLY_COMPLETED = "PARTIALLY_COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REPLANNING = "REPLANNING"
    INVALID = "INVALID"


@dataclass
class AggregateResourceRequirements:
    peak_cpu_cores: float = 0
    peak_memory_mb: int = 0
    peak_gpu_count: int = 0
    peak_gpu_memory_mb: int = 0
    total_disk_mb: int = 0
    network_required: bool = False


@dataclass
class ExecutionStats:
    total_steps: int = 0
    completed_steps: int = 0
    failed_steps: int = 0
    skipped_steps: int = 0
    running_steps: int = 0
    pending_steps: int = 0
    success_rate: float = 0.0
    actual_duration_ms: float = 0.0


@dataclass
class ValidationResult:
    rule_name: str
    passed: bool
    severity: str
    message: str
    affected_steps: list[str] = field(default_factory=list)


@dataclass
class Plan:
    plan_id: str = field(default_factory=lambda: str(uuid4()))
    goal_id: str = ""
    version: int = 1
    title: str = ""
    description: str = ""
    steps: list[PlanStep] = field(default_factory=list)
    root_step_ids: list[str] = field(default_factory=list)
    execution_graph: object = None
    total_estimated_duration_ms: float = 0.0
    total_estimated_cost: float = 0.0
    parallelism_degree: int = 1
    critical_path: list[str] = field(default_factory=list)
    critical_path_duration_ms: float = 0.0
    resource_requirements: AggregateResourceRequirements = field(default_factory=AggregateResourceRequirements)
    status: PlanStatus = PlanStatus.DRAFT
    strategy_used: str = ""
    optimization_score: float = 0.0
    feasibility_score: float = 0.0
    validation_results: list[ValidationResult] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: datetime | None = None
    completed_at: datetime | None = None
    execution_stats: ExecutionStats = field(default_factory=ExecutionStats)
    metadata: dict = field(default_factory=dict)
    replanning_history: list[dict] = field(default_factory=list)
