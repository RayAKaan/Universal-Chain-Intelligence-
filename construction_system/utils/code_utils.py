from __future__ import annotations

import ast
import textwrap


def indent(code: str, levels: int = 1, spaces: int = 4) -> str:
    return textwrap.indent(code, " " * (levels * spaces))


def dedent(code: str) -> str:
    return textwrap.dedent(code)


def count_lines(code: str) -> int:
    return len(code.splitlines())


def _safe_parse(code: str):
    try:
        return ast.parse(code)
    except SyntaxError:
        return None


def extract_function_names(code: str) -> list[str]:
    tree = _safe_parse(code)
    if tree is None:
        return []
    return [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]


def extract_class_names(code: str) -> list[str]:
    tree = _safe_parse(code)
    if tree is None:
        return []
    return [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]


def extract_imports(code: str) -> list[str]:
    tree = _safe_parse(code)
    if tree is None:
        return []
    out: list[str] = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            out += [a.name for a in n.names]
        if isinstance(n, ast.ImportFrom):
            out += [n.module or ""]
    return out


def merge_code_blocks(blocks: list[str]) -> str:
    return "\n\n".join(b.strip() for b in blocks if b.strip()) + "\n"


def wrap_in_try_except(code: str, exception_type: str = "Exception") -> str:
    return f"try:\n{textwrap.indent(code, '    ')}\nexcept {exception_type} as exc:\n    raise\n"


def add_logging(code: str, logger_name: str) -> str:
    return f"import logging\nlogger=logging.getLogger('{logger_name}')\n" + code
