from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from enum import Enum
from typing import Any

from capability_system.models.benchmark_result import BenchmarkResult
from capability_system.models.capability import Capability


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)


def serialize_capability(capability: Capability) -> str:
    return json.dumps(capability.to_dict(), cls=EnhancedJSONEncoder)


def deserialize_capability(data: str) -> Capability:
    return Capability.from_dict(json.loads(data))


def serialize_benchmark_result(result: BenchmarkResult) -> str:
    payload = asdict(result)
    payload["timestamp"] = result.timestamp.isoformat()
    return json.dumps(payload, cls=EnhancedJSONEncoder)


def deserialize_benchmark_result(data: str) -> BenchmarkResult:
    payload = json.loads(data)
    payload["timestamp"] = datetime.fromisoformat(payload["timestamp"]) if payload.get("timestamp") else datetime.utcnow()
    return BenchmarkResult(**payload)
