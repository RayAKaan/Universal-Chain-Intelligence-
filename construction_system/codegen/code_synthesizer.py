from __future__ import annotations

import textwrap


class CodeSynthesizer:
    def synthesize_import_block(self, imports):
        lines = []
        for i in imports:
            if i.get("names"):
                lines.append(f"from {i['module']} import {', '.join(i['names'])}")
            else:
                lines.append(f"import {i['module']}")
        return "\n".join(lines)

    def synthesize_function(self, name, parameters, return_type, body_lines, docstring="", decorators=None, is_async=False):
        decorators = decorators or []
        params = ", ".join(
            f"{p.get('name')}"
            + (f": {p.get('type')}" if p.get("type") else "")
            + (f"={repr(p.get('default'))}" if "default" in p else "")
            for p in parameters
        )
        head = "\n".join([f"@{d}" for d in decorators])
        kind = "async def" if is_async else "def"
        body = "\n".join(body_lines) if body_lines else "pass"
        doc = f'    """{docstring}"""\n' if docstring else ""
        return f"{head + chr(10) if head else ''}{kind} {name}({params}) -> {return_type}:\n{doc}{textwrap.indent(body, '    ')}\n"

    def synthesize_class(self, name, base_classes, methods, properties, class_variables, docstring="", decorators=None):
        decorators = decorators or []
        bases = ", ".join(base_classes) if base_classes else "object"
        lines = [f"@{d}" for d in decorators] + [f"class {name}({bases}):", f"    \"\"\"{docstring}\"\"\"" if docstring else "    pass"]
        for v in class_variables:
            lines.append(f"    {v['name']} = {repr(v.get('value'))}")
        for p in properties:
            lines.append(f"    @property\n    def {p['name']}(self):\n        {p.get('getter', 'return None')}")
        for m in methods:
            lines.append(textwrap.indent(m.get("code", "def x(self):\n    pass"), "    "))
        return "\n".join(lines) + "\n"

    def synthesize_dataclass(self, name, fields, methods=None, docstring=""):
        methods = methods or []
        f = "\n".join(f"    {x['name']}: {x.get('type', 'object')}" for x in fields)
        ms = "\n".join(methods)
        return f"from dataclasses import dataclass\n@dataclass\nclass {name}:\n{f or '    pass'}\n{ms}\n"

    def synthesize_enum(self, name, members, docstring=""):
        m = "\n".join(f"    {x['name']} = {repr(x.get('value', x['name']))}" for x in members)
        return f"from enum import Enum\nclass {name}(str, Enum):\n{m}\n"

    def synthesize_main_block(self, entry_function, args=None):
        args = args or []
        return f"if __name__ == '__main__':\n    {entry_function}({', '.join(args)})\n"

    def synthesize_try_except(self, try_body, except_clauses, finally_body=None):
        s = "try:\n" + textwrap.indent("\n".join(try_body), "    ") + "\n"
        for e in except_clauses:
            s += f"except {e.get('type', 'Exception')} as {e.get('name', 'exc')}:\n" + textwrap.indent("\n".join(e.get("body", ["raise"])), "    ") + "\n"
        if finally_body:
            s += "finally:\n" + textwrap.indent("\n".join(finally_body), "    ") + "\n"
        return s

    def synthesize_context_manager(self, name, init_params, enter_body, exit_body):
        return f"class {name}:\n    def __enter__(self):\n{textwrap.indent(chr(10).join(enter_body), '        ')}\n    def __exit__(self, exc_type, exc, tb):\n{textwrap.indent(chr(10).join(exit_body), '        ')}\n"

    def synthesize_decorator(self, name, parameters, wrapper_body):
        return f"def {name}(fn):\n    def wrapper(*args, **kwargs):\n{textwrap.indent(chr(10).join(wrapper_body), '        ')}\n    return wrapper\n"

    def synthesize_property(self, name, type, getter_body, setter_body=None):
        s = f"@property\ndef {name}(self) -> {type}:\n{textwrap.indent(chr(10).join(getter_body), '    ')}\n"
        if setter_body:
            s += f"@{name}.setter\ndef {name}(self, value):\n{textwrap.indent(chr(10).join(setter_body), '    ')}\n"
        return s
