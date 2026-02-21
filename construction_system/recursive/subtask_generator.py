from __future__ import annotations

from construction_system.models.component import Component
from construction_system.models.specification import ComponentSpec, Specification, SpecType


class SubtaskGenerator:
    def should_decompose(self, spec: Specification) -> bool:
        return spec.spec_type == SpecType.COMPOSITE_SYSTEM

    def decompose_composite_spec(self, spec: Specification) -> list[Specification]:
        subtasks: list[Specification] = []
        for c in spec.components:
            try:
                child_type = SpecType(c.component_type)
            except Exception:
                child_type = SpecType.MODULE
            subtasks.append(
                Specification(
                    name=c.name,
                    spec_type=child_type,
                    description=f"Child component of {spec.name}",
                    configuration=dict(spec.configuration),
                    metadata=dict(spec.metadata),
                )
            )
        return subtasks

    def generate_subtasks(self, spec: Specification) -> list[Specification]:
        if spec.spec_type == SpecType.COMPOSITE_SYSTEM:
            return self.decompose_composite_spec(spec)
        return []

    def generate_test_spec(self, spec: Specification) -> Specification:
        return Specification(
            name=f"{spec.name}_tests",
            spec_type=SpecType.MODULE,
            description="Generated tests",
            configuration=dict(spec.configuration),
            metadata=dict(spec.metadata),
        )

    def generate_integration_spec(self, components: list[Component]) -> Specification:
        s = Specification(
            name="integration_system",
            spec_type=SpecType.COMPOSITE_SYSTEM,
            description="Auto-generated integration system",
        )
        s.components = [
            ComponentSpec(
                component_id=c.component_id,
                name=c.name,
                component_type=SpecType.MODULE.value,
                specification={"entry_point": c.entry_point},
                dependencies=[],
            )
            for c in components
        ]
        return s
