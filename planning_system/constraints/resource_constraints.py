from __future__ import annotations


def MaxCPUConstraint(plan, value):
    peak = plan.resource_requirements.peak_cpu_cores
    return peak <= value, peak


def MaxMemoryConstraint(plan, value):
    peak = plan.resource_requirements.peak_memory_mb
    return peak <= value, peak


def MaxGPUConstraint(plan, value):
    peak = plan.resource_requirements.peak_gpu_count
    return peak <= value, peak


def MaxDiskConstraint(plan, value):
    peak = plan.resource_requirements.total_disk_mb
    return peak <= value, peak
