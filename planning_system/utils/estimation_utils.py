from __future__ import annotations


def classify_complexity(step_description: str) -> str:
    t = step_description.lower()
    if any(k in t for k in ["train", "deploy", "optimize", "distributed", "parallel"]):
        return "complex"
    if any(k in t for k in ["transform", "analyze", "validate"]):
        return "medium"
    return "simple"


def estimate_duration_from_complexity(step_description: str) -> float:
    c = classify_complexity(step_description)
    return {"simple": 1000.0, "medium": 5000.0, "complex": 30000.0}[c]


def estimate_resource_requirements(step_description: str) -> dict:
    c = classify_complexity(step_description)
    return {
        "simple": {"cpu": 0.2, "memory_mb": 128},
        "medium": {"cpu": 1.0, "memory_mb": 1024},
        "complex": {"cpu": 2.0, "memory_mb": 4096},
    }[c]
