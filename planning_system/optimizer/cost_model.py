from __future__ import annotations

from planning_system import config


def estimate_resource_cost(resources, duration_ms: float) -> float:
    hours = duration_ms / 3_600_000
    cpu = getattr(resources, "min_cpu_cores", 0.1)
    mem = getattr(resources, "min_memory_mb", 64) / 1024
    gpu = 1 if getattr(resources, "requires_gpu", False) else 0
    return cpu * config.COST_CPU_PER_CORE_HOUR * hours + mem * config.COST_MEMORY_PER_GB_HOUR * hours + gpu * config.COST_GPU_PER_HOUR * hours


def estimate_step_cost(step) -> float:
    base = config.COST_API_CALL if "api" in step.execution_type.lower() else 0.0
    return base + estimate_resource_cost(step.resource_requirements or object(), step.estimated_duration_ms)


def estimate_plan_cost(plan) -> float:
    return sum(estimate_step_cost(s) for s in plan.steps if s.is_leaf)
