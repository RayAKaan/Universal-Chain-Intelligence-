from __future__ import annotations

import time
from pathlib import Path

from construction_system.construction.base_constructor import BaseConstructor
from construction_system.models.artifact import ArtifactType
from construction_system.models.blueprint import Blueprint
from construction_system.models.build_result import BuildResult, BuildStatus
from construction_system.models.specification import SpecType
from construction_system.utils.code_utils import count_lines, extract_class_names, extract_function_names
from construction_system.utils.file_utils import create_directory, write_file


class BlueprintError(Exception):
    pass


class SystemConstructor(BaseConstructor):
    constructor_name = "system_constructor"
    supported_spec_types = [
        SpecType.MODULE,
        SpecType.PACKAGE,
        SpecType.COMPOSITE_SYSTEM,
        SpecType.FUNCTION,
        SpecType.CLASS,
        SpecType.CONFIGURATION,
        SpecType.SCRIPT,
        SpecType.DOCKERFILE,
        SpecType.API,
    ]

    def __init__(self, code_generator, validator, sandbox, artifact_manager, composer, config):
        self.codegen = code_generator
        self.validator = validator
        self.sandbox = sandbox
        self.artifact_manager = artifact_manager
        self.composer = composer
        self.config = config

    def _template_variables_for_spec(self, spec) -> dict:
        st = spec.spec_type.value
        if st == "FUNCTION":
            params = ", ".join(f"{p.name}: {p.data_type}" for p in spec.inputs)
            body = "\n".join(spec.metadata.get("body_lines", ["return {}"]))
            return {
                "function_name": spec.name,
                "async_prefix": "async def" if spec.metadata.get("is_async") else "def",
                "parameters": params,
                "return_type": spec.outputs[0].data_type if spec.outputs else "dict",
                "docstring": spec.description or spec.name,
                "decorators": "\n".join(spec.metadata.get("decorators", [])),
                "body": body,
            }
        if st == "CLASS":
            methods = []
            for m in spec.metadata.get("methods", []):
                m_params = ", ".join(["self"] + [p.get("name", "arg") for p in m.get("params", [])])
                m_body = "\n".join(f"        {line}" for line in m.get("body", ["return None"]))
                methods.append(f"def {m.get('name', 'method')}({m_params}) -> {m.get('return_type', 'None')}:\n{m_body}")
            init_params = "".join(f", {p.get('name', 'arg')}: {p.get('type', 'Any')}" for p in spec.metadata.get("init_params", []))
            init_body = "\n".join([f"self.{p.get('name', 'arg')} = {p.get('name', 'arg')}" for p in spec.metadata.get("init_params", [])]) or "pass"
            return {
                "class_name": spec.name,
                "base_classes": ", ".join(spec.metadata.get("base_classes", ["object"])),
                "init_params": init_params,
                "init_body": init_body,
                "methods": "\n\n".join(methods) if methods else "def process(self):\n        return None",
                "docstring": spec.description or spec.name,
            }
        if st == "CAPABILITY_PLUGIN":
            return {
                "plugin_name": spec.name.title().replace("_", ""),
                "processing_logic": "\n".join(spec.metadata.get("processing_logic", ["return payload"])),
            }
        if st == "STRATEGY_PLUGIN":
            return {
                "strategy_name": spec.name,
                "description": spec.description or spec.name,
                "planning_logic": "\n".join(spec.metadata.get("planning_logic", ["return None"])),
                "suitability": repr(spec.metadata.get("suitability", True)),
            }
        if st == "CLI_TOOL":
            return {
                "tool_name": spec.name,
                "description": spec.description or spec.name,
                "commands": "\n".join(spec.configuration.get("commands", ["default"])),
                "arguments": "",
            }
        return {
            "function_name": "run",
            "async_prefix": "def",
            "parameters": "",
            "return_type": "dict",
            "docstring": spec.description or spec.name,
            "decorators": "",
            "body": "return {'ok': True}",
        }

    def generate_blueprint(self, spec):
        bp = Blueprint(spec_id=spec.spec_id, name=spec.name)
        module = spec.configuration.get("target_directory", "constructed/") + "/" + spec.name.lower().replace(" ", "_")
        template_id = spec.metadata.get("template_id", "python_function")
        bp.directory_structure = [module, module + "/tests"]
        bp.file_plan = [
            {
                "file_path": module + "/main.py",
                "file_type": "python",
                "purpose": "entry",
                "code_units": [],
                "template_id": template_id,
                "template_variables": self._template_variables_for_spec(spec),
            }
        ]
        bp.build_order = [x["file_path"] for x in bp.file_plan]
        bp.estimated_lines_of_code = 30
        return bp

    def build_from_blueprint(self, blueprint, context):
        start = time.time()
        result = BuildResult(blueprint_id=blueprint.blueprint_id, spec_id=blueprint.spec_id, status=BuildStatus.SUCCESS, blueprint=blueprint)
        for d in blueprint.directory_structure:
            create_directory(d)
        generated = self.codegen.generate_from_blueprint(blueprint)
        for path, code in generated.items():
            write_file(path, code)
            result.files_created.append(path)
        code_units = self.codegen.generate(type("S", (), {"spec_type": type("T", (), {"value": "FUNCTION"})(), "name": "generated", "inputs": [], "outputs": [], "description": "", "metadata": {}, "configuration": {}})())
        result.code_units = code_units
        report = self.validator.validate(code_units, blueprint)
        result.validation_results["syntax_valid"] = report.is_valid
        if not report.is_valid:
            result.status = BuildStatus.VALIDATION_FAILED
            result.errors += [i.message for i in report.issues]
        sb = self.sandbox.execute_file_in_sandbox(result.files_created[0]) if result.files_created else None
        result.sandbox_results = sb.__dict__ if sb else {}
        result.code_stats = {
            "total_files": len(result.files_created),
            "total_lines": sum(count_lines(Path(f).read_text()) for f in result.files_created),
            "total_functions": sum(len(extract_function_names(Path(f).read_text())) for f in result.files_created),
            "total_classes": sum(len(extract_class_names(Path(f).read_text())) for f in result.files_created),
            "total_tests": 0,
        }
        for f in result.files_created:
            a = self.artifact_manager.register_artifact(Path(f).name, f, ArtifactType.SOURCE_CODE, result.spec_id, result.blueprint_id, {})
            result.artifacts_created.append(a.artifact_id)
            result.artifacts.append(a)
        result.build_duration_ms = (time.time() - start) * 1000
        return result

    def construct(self, spec, context):
        bp = self.generate_blueprint(spec)
        return self.build_from_blueprint(bp, context)
