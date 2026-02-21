from __future__ import annotations

from construction_system.construction.system_constructor import SystemConstructor
from construction_system.models.specification import SpecType


class ServiceConstructor(SystemConstructor):
    constructor_name = "service_constructor"
    supported_spec_types = [SpecType.SERVICE, SpecType.API]

    def generate_service_class(self, spec):
        return [
            f"class {spec.name.title().replace('_', '')}Service:\n"
            "    def start(self):\n"
            "        return True\n"
            "    def stop(self):\n"
            "        return True\n"
        ]
