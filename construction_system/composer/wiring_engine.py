from __future__ import annotations

from construction_system.models.code_unit import CodeUnit


class WiringEngine:
    def determine_initialization_order(self, composition):
        return composition.initialization_order or composition.components

    def generate_adapter(self, source_interface, target_interface):
        return CodeUnit(name="adapter", code="class Adapter:\n    def adapt(self, value):\n        return value\n")

    def generate_wiring_code(self, composition):
        lines = ["# auto wiring"]
        for w in composition.wirings:
            lines.append(f"# {w['source_component_id']}.{w['source_method']} -> {w['target_component_id']}.{w['target_method']}")
        return [CodeUnit(name="integration_wiring", code="\n".join(lines) + "\n")]
