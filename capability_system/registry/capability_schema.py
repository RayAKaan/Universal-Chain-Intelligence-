from __future__ import annotations

from collections import defaultdict

from capability_system.models.capability import Capability
from capability_system.utils.validators import validate_json_schema, validate_semver


class CapabilityValidationError(ValueError):
    pass


def validate_capability(capability: Capability) -> None:
    required = [capability.name, capability.version, capability.execution_endpoint]
    if any(not v for v in required):
        raise CapabilityValidationError("name, version, and execution_endpoint are required")
    if not validate_semver(capability.version):
        raise CapabilityValidationError(f"Invalid semantic version: {capability.version}")
    if not validate_json_schema(capability.input_schema):
        raise CapabilityValidationError("input_schema is not valid JSON schema")
    if not validate_json_schema(capability.output_schema):
        raise CapabilityValidationError("output_schema is not valid JSON schema")
    _ensure_no_circular_dependencies(capability.capability_id, capability.dependencies)


def _ensure_no_circular_dependencies(capability_id: str, dependencies: list[str]) -> None:
    graph = defaultdict(list)
    for dep in dependencies:
        graph[capability_id].append(dep)
    visiting: set[str] = set()

    def dfs(node: str) -> None:
        if node in visiting:
            raise CapabilityValidationError("Circular dependency detected")
        visiting.add(node)
        for nxt in graph.get(node, []):
            dfs(nxt)
        visiting.remove(node)

    dfs(capability_id)
