from __future__ import annotations

from planning_system.resolver.resolution_strategies import CompositeMatchStrategy


class CapabilityResolutionError(Exception):
    pass


class UnresolvableStepError(CapabilityResolutionError):
    pass


class CapabilityResolver:
    def __init__(self, capability_registry, query_engine, config):
        self.registry = capability_registry
        self.query_engine = query_engine
        self.config = config
        self.strategy = CompositeMatchStrategy()

    def resolve_plan(self, plan):
        for step in plan.steps:
            if step.is_leaf:
                self.resolve_step(step)
        unresolved = self.get_unresolvable_steps(plan)
        if unresolved:
            raise UnresolvableStepError(", ".join(s.name for s in unresolved))
        return plan

    def resolve_step(self, step, context=None):
        candidates = self.find_candidates(step)
        cap = self.select_best(candidates)
        if not cap:
            return step
        step.capability_id = cap.capability_id
        step.capability_name = cap.name
        step.execution_type = cap.execution_type.value
        step.estimated_duration_ms = cap.performance_profile.avg_latency_ms or step.estimated_duration_ms
        step.resource_requirements = cap.resource_requirements
        return step

    def find_candidates(self, step):
        caps = [c for c in self.registry.get_all() if c.is_enabled]
        scored = [(c, self.strategy.score(step, c)) for c in caps]
        return sorted(scored, key=lambda x: x[1], reverse=True)

    def select_best(self, candidates, constraints=None):
        if not candidates:
            return None
        filtered = [c for c, s in candidates if s > 0.25]
        return filtered[0] if filtered else candidates[0][0]

    def resolve_with_fallbacks(self, step):
        candidates = self.find_candidates(step)
        primary = self.resolve_step(step)
        fallbacks = []
        for cap, score in candidates[1:3]:
            fb = step.__class__(**{**step.__dict__, "step_id": step.step_id + "-fb-" + cap.capability_id[:4], "capability_id": cap.capability_id, "capability_name": cap.name})
            fallbacks.append(fb)
        return primary, fallbacks

    def get_unresolvable_steps(self, plan):
        return [s for s in plan.steps if s.is_leaf and not s.capability_id]

    def suggest_missing_capabilities(self, step):
        return [{"name": step.name, "category": "suggested", "reason": "No capability matched"}]
