from __future__ import annotations

import re


class CodeFormatter:
    def normalize_indentation(self, code, indent=4):
        return "\n".join(line.replace("\t", " " * indent) for line in code.splitlines())

    def remove_trailing_whitespace(self, code):
        return "\n".join(l.rstrip() for l in code.splitlines())

    def ensure_newline_at_end(self, code):
        return code if code.endswith("\n") else code + "\n"

    def format_imports(self, imports):
        std = sorted([i for i in imports if "." not in i])
        third = sorted([i for i in imports if "." in i and not i.startswith("construction_system")])
        local = sorted([i for i in imports if i.startswith("construction_system")])
        return "\n".join([*(f"import {i}" for i in std), "", *(f"import {i}" for i in third), "", *(f"import {i}" for i in local)]).strip() + "\n"

    def add_file_header(self, code, module_name, description):
        return f'"""{module_name}: {description}. Auto-generated."""\n\n' + code

    def format_code(self, code, language="python"):
        c = self.normalize_indentation(code)
        c = self.remove_trailing_whitespace(c)
        c = re.sub(r"\n{3,}", "\n\n", c)
        return self.ensure_newline_at_end(c)
