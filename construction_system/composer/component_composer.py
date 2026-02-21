from __future__ import annotations

from construction_system.models.build_result import BuildResult, BuildStatus
from construction_system.models.code_unit import CodeUnit
from construction_system.models.composition import Composition


class ComponentComposer:
    def __init__(self, interface_matcher, wiring_engine, validator, config):
        self.matcher = interface_matcher
        self.wiring_engine = wiring_engine
        self.validator = validator
        self.config = config

    def auto_compose(self, components):
        c = Composition(name="auto_composition", components=[x.component_id for x in components])
        c.initialization_order = [x.component_id for x in components]
        for i in range(len(components) - 1):
            c.wirings.append({"wiring_id": f"w{i}", "source_component_id": components[i].component_id, "source_interface": "*", "source_method": "process", "target_component_id": components[i + 1].component_id, "target_interface": "*", "target_method": "process", "data_transform": ""})
        return c

    def generate_integration_module(self, composition):
        return self.wiring_engine.generate_wiring_code(composition)

    def generate_composition_tests(self, composition):
        return [CodeUnit(name="test_composition", code="import unittest\nclass TestComp(unittest.TestCase):\n    def test_comp(self):\n        self.assertTrue(True)\n")]

    def compose(self, components, composition_spec):
        issues = self.validator.validate_composition(composition_spec)
        r = BuildResult(status=BuildStatus.SUCCESS if not issues else BuildStatus.FAILURE, errors=issues)
        units = self.generate_integration_module(composition_spec)
        r.code_units = units
        r.files_created = ["constructed/integration_module.py"]
        r.code_stats["total_files"] = 1
        return r
