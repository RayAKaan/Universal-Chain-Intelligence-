from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

class MetricType(str, Enum):
    LATENCY='LATENCY'; THROUGHPUT='THROUGHPUT'; SUCCESS_RATE='SUCCESS_RATE'; ERROR_RATE='ERROR_RATE'; RESOURCE_USAGE_CPU='RESOURCE_USAGE_CPU'; RESOURCE_USAGE_MEMORY='RESOURCE_USAGE_MEMORY'; RESOURCE_USAGE_GPU='RESOURCE_USAGE_GPU'; RESOURCE_USAGE_DISK='RESOURCE_USAGE_DISK'; QUEUE_DEPTH='QUEUE_DEPTH'; EXECUTION_TIME='EXECUTION_TIME'; PLANNING_TIME='PLANNING_TIME'; RESOLUTION_TIME='RESOLUTION_TIME'; CONSTRUCTION_TIME='CONSTRUCTION_TIME'; BENCHMARK_SCORE='BENCHMARK_SCORE'; CAPABILITY_COUNT='CAPABILITY_COUNT'; ACTIVE_CAPABILITY_COUNT='ACTIVE_CAPABILITY_COUNT'; HEALTHY_CAPABILITY_COUNT='HEALTHY_CAPABILITY_COUNT'; PLAN_COMPLEXITY='PLAN_COMPLEXITY'; STEP_COUNT='STEP_COUNT'; PARALLEL_EFFICIENCY='PARALLEL_EFFICIENCY'; CACHE_HIT_RATE='CACHE_HIT_RATE'; DISCOVERY_COUNT='DISCOVERY_COUNT'; BUILD_SUCCESS_RATE='BUILD_SUCCESS_RATE'; TEST_PASS_RATE='TEST_PASS_RATE'; SANDBOX_SUCCESS_RATE='SANDBOX_SUCCESS_RATE'; IMPROVEMENT_COUNT='IMPROVEMENT_COUNT'; REGRESSION_COUNT='REGRESSION_COUNT'; CUSTOM='CUSTOM'

@dataclass
class Metric:
    name: str
    metric_type: MetricType
    source_phase: str
    source_component: str
    value: float
    unit: str = ''
    metric_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    window_start: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    window_end: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    window_duration_seconds: float = 0.0
    tags: dict = field(default_factory=dict)
    context: dict = field(default_factory=dict)
