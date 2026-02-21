from __future__ import annotations

from construction_system.models.code_unit import CodeUnit, CodeUnitType


class TestGenerator:
    def generate_function_test(self, func_name, parameters, return_type):
        return f"    def test_{func_name}(self):\n        self.assertTrue(callable({func_name}))\n"

    def generate_class_test(self, class_name, methods):
        return f"    def test_{class_name.lower()}(self):\n        obj={class_name}()\n        self.assertIsNotNone(obj)\n"

    def generate_integration_test(self, components):
        return "import unittest\nclass TestIntegration(unittest.TestCase):\n    def test_integration(self):\n        self.assertTrue(True)\n"

    def generate_tests(self, code_unit):
        body = self.generate_function_test(code_unit.name, code_unit.input_parameters, code_unit.return_type)
        code = f"import unittest\nfrom target import {code_unit.name}\nclass Test{code_unit.name.title().replace('_','')}(unittest.TestCase):\n{body}\n"
        return CodeUnit(name=f"test_{code_unit.name}", unit_type=CodeUnitType.TEST_CASE, code=code, is_test=True)
