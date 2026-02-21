from __future__ import annotations

from construction_system.construction.system_constructor import SystemConstructor
from construction_system.models.code_unit import CodeUnit
from construction_system.models.specification import SpecType


class PipelineConstructor(SystemConstructor):
    constructor_name = "pipeline_constructor"
    supported_spec_types = [SpecType.PIPELINE]

    def generate_pipeline_class(self, name, stages):
        body = "\n".join([
            "class Stage:",
            "    def process(self, x):",
            "        return x",
            f"class {name}:",
            "    def __init__(self):",
            "        self.stages=[]",
            "    def run(self, data):",
            "        for s in self.stages: data=s.process(data)",
            "        return data",
        ])
        return CodeUnit(name=name, unit_type="CLASS", code=body)

    def generate_stage(self, stage_spec):
        return CodeUnit(name=stage_spec.get("name", "Stage"), code=f"class {stage_spec.get('name', 'Stage')}:\n    def process(self, data):\n        return data\n")

    def generate_pipeline_config(self, stages):
        return CodeUnit(name="pipeline_config", code="PIPELINE_STAGES=" + repr(stages) + "\n")
