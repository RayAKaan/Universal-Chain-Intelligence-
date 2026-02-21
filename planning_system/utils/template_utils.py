from __future__ import annotations

from copy import deepcopy


def apply_template(template: dict, variables: dict) -> dict:
    out = deepcopy(template)
    for k, v in out.items():
        if isinstance(v, str):
            for vk, vv in variables.items():
                out[k] = out[k].replace("{{" + vk + "}}", str(vv))
    return out


def merge_templates(base: dict, override: dict) -> dict:
    out = deepcopy(base)
    out.update(override)
    return out


def validate_template(template: dict) -> bool:
    return isinstance(template, dict) and len(template) > 0
