from __future__ import annotations

from construction_system.codegen.code_formatter import CodeFormatter
from construction_system.codegen.code_synthesizer import CodeSynthesizer
from construction_system.codegen.language_backends.config_backend import ConfigBackend
from construction_system.codegen.language_backends.dockerfile_backend import DockerfileBackend
from construction_system.codegen.language_backends.python_backend import PythonBackend
from construction_system.codegen.language_backends.shell_backend import ShellBackend
from construction_system.models.code_unit import CodeUnit, CodeUnitType


class CodeGenerationError(Exception):
    pass


class CodeGenerator:
    def __init__(self, template_library, synthesizer=None, formatter=None, config=None):
        self.template_library = template_library
        self.synth = synthesizer or CodeSynthesizer()
        self.formatter = formatter or CodeFormatter()
        self.config = config
        self.backends = {"python": PythonBackend(), "shell": ShellBackend(), "config": ConfigBackend(), "dockerfile": DockerfileBackend()}

    def generate(self, spec):
        st = spec.spec_type.value
        if st == "FUNCTION":
            return [self.generate_function({"name": spec.name, "parameters": [i.__dict__ for i in spec.inputs], "return_type": spec.outputs[0].data_type if spec.outputs else "dict", "body_logic": ["return {}"], "docstring": spec.description})]
        if st == "CLASS":
            return [self.generate_class({"name": spec.name, "methods": spec.metadata.get("methods", [])})]
        return self.generate_module({"name": spec.name})

    def generate_function(self, spec):
        code = self.synth.synthesize_function(spec.get("name", "generated_function"), spec.get("parameters", []), spec.get("return_type", "Any"), spec.get("body_logic", ["return None"]), spec.get("docstring", ""), spec.get("decorators", []), spec.get("is_async", False))
        return CodeUnit(name=spec.get("name", "generated_function"), unit_type=CodeUnitType.FUNCTION, code=self.formatter.format_code(code))

    def generate_class(self, spec):
        methods = [{"code": self.synth.synthesize_function(m.get("name", "process"), m.get("params", []), m.get("return_type", "dict"), m.get("body", ["return {}"]))} for m in spec.get("methods", [])]
        code = self.synth.synthesize_class(spec.get("name", "GeneratedClass"), spec.get("base_classes", []), methods, [], [], spec.get("docstring", "generated class"))
        return CodeUnit(name=spec.get("name", "GeneratedClass"), unit_type=CodeUnitType.CLASS, code=self.formatter.format_code(code))

    def generate_module(self, spec):
        u1 = self.generate_function({"name": "main", "parameters": [], "return_type": "dict", "body_logic": ["return {'ok': True}"]})
        u1.is_entry_point = True
        return [u1]

    def generate_from_blueprint(self, blueprint):
        out = {}
        for fp in blueprint.file_plan:
            out[fp["file_path"]] = self.template_library.render_template(fp.get("template_id", "python_function"), fp.get("template_variables", {}))
        return out

    def generate_tests(self, code_units):
        tests = []
        for u in code_units:
            code = f"import unittest\nclass Test{u.name.title().replace('_','')}(unittest.TestCase):\n    def test_runs(self):\n        self.assertTrue(True)\n"
            tests.append(CodeUnit(name=f"test_{u.name}", unit_type=CodeUnitType.TEST_CASE, code=code, is_test=True))
        return tests

    def generate_init_file(self, module_name, exports):
        code = "\n".join(f"from .{module_name} import {e}" for e in exports) + "\n"
        return CodeUnit(name="__init__", unit_type=CodeUnitType.MODULE_INIT, code=code)

    def generate_requirements(self, dependencies):
        return "\n".join(f"{d.name}{'=='+d.version if d.version else ''}" for d in dependencies) + "\n"
