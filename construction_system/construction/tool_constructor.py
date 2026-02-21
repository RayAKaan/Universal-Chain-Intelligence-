from __future__ import annotations

from construction_system.construction.system_constructor import SystemConstructor
from construction_system.models.specification import SpecType


class ToolConstructor(SystemConstructor):
    constructor_name = "tool_constructor"
    supported_spec_types = [SpecType.CLI_TOOL]

    def generate_cli_tool(self, spec):
        description = spec.description or spec.name
        code = "\n".join(
            [
                "import argparse",
                "",
                "",
                "def main() -> None:",
                f"    parser = argparse.ArgumentParser(description={description!r})",
                "    parser.add_argument('command', help='Command to execute')",
                "    args = parser.parse_args()",
                "    print(f'Command: {args.command}')",
                "",
                "",
                "if __name__ == '__main__':",
                "    main()",
                "",
            ]
        )
        return [code]
