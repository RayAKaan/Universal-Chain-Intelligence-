from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from capability_system.utils.hashing import generate_id


@dataclass
class BenchmarkResult:
    result_id: str = field(default_factory=generate_id)
    capability_id: str = ""
    benchmark_suite_id: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    latency_samples: list[float] = field(default_factory=list)
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    min_latency_ms: float = 0.0
    max_latency_ms: float = 0.0
    std_dev_latency_ms: float = 0.0
    throughput_per_second: float = 0.0
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    error_count: int = 0
    timeout_count: int = 0
    reliability: float = 0.0
    resource_usage: dict = field(default_factory=lambda: {
        "peak_cpu_percent": 0.0,
        "peak_memory_mb": 0.0,
        "peak_gpu_percent": 0.0,
        "peak_gpu_memory_mb": 0.0,
    })
    environment: dict = field(default_factory=dict)
    notes: str = ""
    is_valid: bool = True
