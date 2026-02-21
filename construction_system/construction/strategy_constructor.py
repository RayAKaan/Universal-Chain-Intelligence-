from __future__ import annotations

from pathlib import Path

from construction_system.construction.system_constructor import SystemConstructor
from construction_system.models.specification import SpecType


class StrategyConstructor(SystemConstructor):
    constructor_name = "strategy_constructor"
    supported_spec_types = [SpecType.STRATEGY_PLUGIN]

    def generate_strategy_class(self, spec):
        name = spec.name.title().replace("_", "")
        logic = "\n        ".join(spec.metadata.get("planning_logic", ["return None"]))
        return (
            "from planning_system.strategies.base_strategy import BaseStrategy\n"
            f"class {name}(BaseStrategy):\n"
            f"    name='{spec.name}'\n"
            f"    description='{spec.description or spec.name}'\n"
            "    def plan(self, goal, context):\n"
            f"        {logic}\n"
            "    def is_suitable(self, goal, context):\n"
            "        return 0.7\n"
        )

    def register_strategy(self, component, spec):
        return spec.name

    def construct(self, spec, context):
        r = super().construct(spec, context)
        p = Path("constructed/strategies") / f"{spec.name}.py"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.generate_strategy_class(spec))
        r.files_created.append(str(p))
        return r
