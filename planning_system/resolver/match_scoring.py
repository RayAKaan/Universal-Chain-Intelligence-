from __future__ import annotations

import re


def _norm(s: str) -> list[str]:
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", s)
    return re.findall(r"[a-z0-9]+", s.lower().replace("_", " "))


def string_similarity(a: str, b: str) -> float:
    sa, sb = set(_norm(a)), set(_norm(b))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def calculate_match_score(step, capability) -> float:
    name = string_similarity(step.name, capability.name)
    typ = 1.0 if ("api" in step.name.lower() and capability.capability_type.value.endswith("API")) else 0.5
    cat = 1.0 if capability.category in step.description.lower() else 0.5 if capability.category in step.name.lower() else 0.0
    io = 0.5
    perf = min(1.0, capability.performance_profile.reliability * 0.7 + (1 / (1 + capability.performance_profile.avg_latency_ms)) * 0.3)
    return 0.35 * name + 0.25 * typ + 0.20 * cat + 0.10 * io + 0.10 * perf
