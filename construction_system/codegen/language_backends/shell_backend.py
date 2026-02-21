from __future__ import annotations

from construction_system.codegen.language_backends.base_backend import BaseBackend


class ShellBackend(BaseBackend):
    language = "shell"
    file_extension = ".sh"

    def generate_file(self, spec, template_vars):
        return "#!/usr/bin/env bash\nset -e\n" + template_vars.get("commands", "echo ok") + "\n"

    def validate_syntax(self, code):
        errs = []
        if not code.startswith("#!/"):
            errs.append("missing shebang")
        return len(errs) == 0, errs
