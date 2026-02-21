from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from capability_system.utils.hashing import generate_fingerprint, generate_id


class CapabilityType(str, Enum):
    PYTHON_FUNCTION = "PYTHON_FUNCTION"
    PYTHON_CLASS = "PYTHON_CLASS"
    SHELL_COMMAND = "SHELL_COMMAND"
    SYSTEM_BINARY = "SYSTEM_BINARY"
    EXTERNAL_SCRIPT = "EXTERNAL_SCRIPT"
    REST_API = "REST_API"
    GRPC_SERVICE = "GRPC_SERVICE"
    MODEL_INFERENCE = "MODEL_INFERENCE"
    PIPELINE = "PIPELINE"
    PLUGIN = "PLUGIN"
    COMPOSITE = "COMPOSITE"


class ExecutionType(str, Enum):
    PYTHON_FUNCTION = "python_function"
    SHELL_COMMAND = "shell_command"
    API_CALL = "api_call"
    MODEL_INFERENCE = "model_inference"
    SCRIPT = "script"
    PLUGIN = "plugin"


class CapabilityState(str, Enum):
    DISCOVERED = "DISCOVERED"
    REGISTERING = "REGISTERING"
    REGISTERED = "REGISTERED"
    BENCHMARKING = "BENCHMARKING"
    BENCHMARKED = "BENCHMARKED"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    DEPRECATED = "DEPRECATED"
    FAILED = "FAILED"
    REMOVED = "REMOVED"


class HealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


@dataclass
class ResourceRequirements:
    min_cpu_cores: float = 0.1
    min_memory_mb: int = 32
    min_disk_mb: int = 0
    requires_gpu: bool = False
    min_gpu_memory_mb: int = 0
    network_required: bool = False
    estimated_bandwidth_mbps: float = 0.0


@dataclass
class PerformanceProfile:
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    throughput_per_second: float = 0.0
    accuracy: float = 0.0
    reliability: float = 0.0
    last_benchmark_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    benchmark_count: int = 0


@dataclass
class Capability:
    capability_id: str = field(default_factory=generate_id)
    name: str = ""
    version: str = "0.0.1"
    capability_type: CapabilityType = CapabilityType.PYTHON_FUNCTION
    category: str = "system"
    subcategory: str = "unknown"
    description: str = ""
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)
    execution_endpoint: str = ""
    execution_type: ExecutionType = ExecutionType.PYTHON_FUNCTION
    execution_config: dict[str, Any] = field(default_factory=dict)
    resource_requirements: ResourceRequirements = field(default_factory=ResourceRequirements)
    performance_profile: PerformanceProfile = field(default_factory=PerformanceProfile)
    metadata: dict[str, Any] = field(default_factory=lambda: {
        "source": "manual", "author": "", "license": "", "tags": [], "documentation_url": "", "repository_url": ""
    })
    state: CapabilityState = CapabilityState.DISCOVERED
    health_status: HealthStatus = HealthStatus.UNKNOWN
    last_health_check: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    dependencies: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_used_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    use_count: int = 0
    error_count: int = 0
    fingerprint: str = ""
    is_enabled: bool = True
    priority_weight: float = 0.5

    def __post_init__(self) -> None:
        if not self.fingerprint:
            self.fingerprint = generate_fingerprint(self)

    def __hash__(self) -> int:
        return hash(self.capability_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Capability) and self.capability_id == other.capability_id

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["capability_type"] = self.capability_type.value
        data["execution_type"] = self.execution_type.value
        data["state"] = self.state.value
        data["health_status"] = self.health_status.value
        for field_name in ["created_at", "updated_at", "last_used_at", "last_health_check"]:
            data[field_name] = getattr(self, field_name).isoformat()
        data["performance_profile"]["last_benchmark_at"] = self.performance_profile.last_benchmark_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Capability":
        cloned = dict(data)
        rr = ResourceRequirements(**cloned.get("resource_requirements", {}))
        pp_data = cloned.get("performance_profile", {})
        pp_data["last_benchmark_at"] = datetime.fromisoformat(pp_data.get("last_benchmark_at", datetime.now(timezone.utc).isoformat()))
        pp = PerformanceProfile(**pp_data)
        for f in ["created_at", "updated_at", "last_used_at", "last_health_check"]:
            cloned[f] = datetime.fromisoformat(cloned[f]) if isinstance(cloned.get(f), str) else cloned.get(f, datetime.now(timezone.utc))
        return cls(
            capability_id=cloned.get("capability_id") or generate_id(),
            name=cloned["name"],
            version=cloned["version"],
            capability_type=CapabilityType(cloned["capability_type"]),
            category=cloned["category"],
            subcategory=cloned["subcategory"],
            description=cloned.get("description", ""),
            input_schema=cloned.get("input_schema", {}),
            output_schema=cloned.get("output_schema", {}),
            execution_endpoint=cloned.get("execution_endpoint", ""),
            execution_type=ExecutionType(cloned["execution_type"]),
            execution_config=cloned.get("execution_config", {}),
            resource_requirements=rr,
            performance_profile=pp,
            metadata=cloned.get("metadata", {}),
            state=CapabilityState(cloned.get("state", CapabilityState.DISCOVERED.value)),
            health_status=HealthStatus(cloned.get("health_status", HealthStatus.UNKNOWN.value)),
            last_health_check=cloned.get("last_health_check", datetime.now(timezone.utc)),
            dependencies=cloned.get("dependencies", []),
            conflicts=cloned.get("conflicts", []),
            alternatives=cloned.get("alternatives", []),
            created_at=cloned.get("created_at", datetime.now(timezone.utc)),
            updated_at=cloned.get("updated_at", datetime.now(timezone.utc)),
            last_used_at=cloned.get("last_used_at", datetime.now(timezone.utc)),
            use_count=cloned.get("use_count", 0),
            error_count=cloned.get("error_count", 0),
            fingerprint=cloned.get("fingerprint", ""),
            is_enabled=bool(cloned.get("is_enabled", True)),
            priority_weight=float(cloned.get("priority_weight", 0.5)),
        )

    def clone(self) -> "Capability":
        return deepcopy(self)
