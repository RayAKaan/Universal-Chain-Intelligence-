from __future__ import annotations

from planning_system.optimizer.cost_model import estimate_plan_cost
from planning_system.optimizer.optimization_strategies import (
    CriticalPathOptimizer,
    GreedyOptimizer,
    ParallelismMaximizer,
    ResourceBalancer,
)
from planning_system.optimizer.resource_estimator import estimate_plan_peak_resources


class PlanOptimizer:
    def __init__(self, cost_model, resource_estimator, config):
        self.cost_model = cost_model
        self.resource_estimator = resource_estimator
        self.config = config

    def optimize(self, plan, objectives=None):
        objectives = objectives or ["minimize_duration", "minimize_cost", "maximize_reliability"]
        plan = self.optimize_parallelism(plan)
        plan = self.optimize_resource_usage(plan)
        plan = self.optimize_cost(plan)
        plan = self.optimize_reliability(plan)
        metrics = self.estimate_plan_metrics(plan)
        plan.total_estimated_duration_ms = metrics["duration_ms"]
        plan.total_estimated_cost = metrics["cost"]
        plan.optimization_score = min(1.0, 1 / (1 + plan.total_estimated_duration_ms / 10000) + 0.2)
        return plan

    def optimize_parallelism(self, plan):
        return ParallelismMaximizer().optimize(plan)

    def optimize_resource_usage(self, plan):
        return ResourceBalancer().optimize(plan)

    def optimize_cost(self, plan):
        return GreedyOptimizer().optimize(plan)

    def optimize_reliability(self, plan):
        for s in plan.steps:
            s.retry_policy.max_retries = max(2, s.retry_policy.max_retries)
        return CriticalPathOptimizer().optimize(plan)

    def estimate_plan_metrics(self, plan):
        duration = sum(s.estimated_duration_ms for s in plan.steps)
        return {
            "duration_ms": duration,
            "cost": estimate_plan_cost(plan),
            "resource": estimate_plan_peak_resources(plan),
        }
