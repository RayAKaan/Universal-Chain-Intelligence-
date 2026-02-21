from __future__ import annotations

import json
from pathlib import Path

from construction_system.construction.system_constructor import SystemConstructor
from construction_system.models.specification import SpecType


class CapabilityConstructor(SystemConstructor):
    constructor_name = "capability_constructor"
    supported_spec_types = [SpecType.CAPABILITY_PLUGIN]

    def generate_manifest(self, spec):
        return {
            "name": spec.name,
            "version": spec.version,
            "description": spec.description,
            "category": spec.metadata.get("category", "data"),
            "subcategory": spec.metadata.get("subcategory", "processing"),
            "entry_point": "plugin.py",
            "class_name": spec.name.title().replace("_", ""),
            "input_schema": spec.metadata.get("input_schema", {}),
            "output_schema": spec.metadata.get("output_schema", {}),
            "dependencies": [],
            "resource_requirements": {},
        }

    def generate_capability_plugin(self, spec):
        cls = spec.name.title().replace("_", "")
        logic = "\n        ".join(spec.metadata.get("processing_logic", ["return payload"]))
        code = f"class {cls}:\n    def execute(self, payload):\n        {logic}\n    def validate(self,payload):\n        return isinstance(payload, dict)\n    def get_requirements(self):\n        return {{'threads':1}}\n"
        return {"plugin.py": code, "manifest.json": json.dumps(self.generate_manifest(spec), indent=2)}

    def register_capability(self, component, spec):
        return component.metadata.get("capability_id", "")

    def construct(self, spec, context):
        r = super().construct(spec, context)
        plugin_dir = Path("plugins") / spec.name
        plugin_dir.mkdir(parents=True, exist_ok=True)
        for fn, code in self.generate_capability_plugin(spec).items():
            (plugin_dir / fn).write_text(code)
            r.files_created.append(str(plugin_dir / fn))
        return r
