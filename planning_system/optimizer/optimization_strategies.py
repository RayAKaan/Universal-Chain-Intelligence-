from __future__ import annotations


class GreedyOptimizer:
    def optimize(self, plan):
        plan.steps.sort(key=lambda s: s.estimated_duration_ms)
        return plan


class ParallelismMaximizer:
    def optimize(self, plan):
        for s in plan.steps:
            if "load" in s.name or "collect" in s.name:
                s.dependencies = []
        return plan


class CriticalPathOptimizer:
    def optimize(self, plan):
        for s in plan.steps:
            if s.estimated_duration_ms > 10000:
                s.estimated_duration_ms *= 0.8
        return plan


class ResourceBalancer:
    def optimize(self, plan):
        plan.steps.sort(key=lambda s: (getattr(getattr(s, "resource_requirements", None), "min_memory_mb", 0), s.name))
        return plan
