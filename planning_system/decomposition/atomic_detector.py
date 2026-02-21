from __future__ import annotations


def find_matching_capabilities(step, capability_registry) -> list:
    caps = capability_registry.get_all()
    n = step.name.lower()
    return [c for c in caps if n in c.name.lower() or any(tok in c.description.lower() for tok in n.split("_"))]


def get_atomicity_score(step, capability_registry) -> float:
    matches = find_matching_capabilities(step, capability_registry)
    if not matches:
        return 0.0
    best = 0.3
    for c in matches:
        if c.name.lower() == step.name.lower():
            best = max(best, 1.0)
        elif step.name.lower() in c.name.lower() or c.name.lower() in step.name.lower():
            best = max(best, 0.7)
        elif c.category in step.description.lower():
            best = max(best, 0.5)
    return best


def is_atomic(step, capability_registry) -> bool:
    return get_atomicity_score(step, capability_registry) >= 0.5
