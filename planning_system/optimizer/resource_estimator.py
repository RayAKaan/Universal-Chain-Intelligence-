from __future__ import annotations

from planning_system.models.plan import AggregateResourceRequirements


def estimate_step_resources(step):
    rr = step.resource_requirements
    if rr is None:
        return {"min_cpu_cores": 0.2, "min_memory_mb": 128}
    return {
        "min_cpu_cores": getattr(rr, "min_cpu_cores", 0.2) * 1.1,
        "min_memory_mb": int(getattr(rr, "min_memory_mb", 128) * 1.1),
    }


def estimate_plan_peak_resources(plan):
    peak_cpu = 0.0
    peak_mem = 0
    for s in plan.steps:
        r = estimate_step_resources(s)
        peak_cpu = max(peak_cpu, r["min_cpu_cores"])
        peak_mem = max(peak_mem, r["min_memory_mb"])
    return AggregateResourceRequirements(peak_cpu_cores=peak_cpu, peak_memory_mb=peak_mem)


def check_resource_feasibility(plan, available_resources: dict):
    issues = []
    peak = estimate_plan_peak_resources(plan)
    if peak.peak_cpu_cores > available_resources.get("available_threads", 4):
        issues.append("peak cpu exceeds available threads")
    if peak.peak_memory_mb > available_resources.get("memory_available_bytes", 1_000_000_000) / (1024 * 1024):
        issues.append("peak memory exceeds available")
    return (len(issues) == 0, issues)
