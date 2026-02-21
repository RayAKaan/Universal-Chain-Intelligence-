from __future__ import annotations


class Phase1Adapter:
    def __init__(self, capability_registry, query_engine, benchmark_engine):
        self.registry = capability_registry
        self.query_engine = query_engine
        self.benchmark_engine = benchmark_engine

    def get_capabilities_for_step(self, step):
        cands = self.query_engine.search(step.name)
        return [c for c in cands if c.is_enabled and c.health_status.value in {"HEALTHY", "UNKNOWN"}]

    def get_capability_performance(self, capability_id):
        return self.registry.get(capability_id).performance_profile

    def get_all_active_capabilities(self):
        return self.registry.get_active() or self.registry.get_all()

    def get_capabilities_by_category(self, category):
        return self.registry.get_by_category(category)

    def check_capability_available(self, capability_id):
        if not self.registry.exists(capability_id):
            return False
        cap = self.registry.get(capability_id)
        return cap.is_enabled and cap.state.value in {"ACTIVE", "REGISTERED", "BENCHMARKED"}

    def get_capability_summary(self):
        caps = self.registry.get_all()
        by_type = {}
        by_category = {}
        for c in caps:
            by_type[c.capability_type.value] = by_type.get(c.capability_type.value, 0) + 1
            by_category[c.category] = by_category.get(c.category, 0) + 1
        return {"by_type": by_type, "by_category": by_category, "count": len(caps)}
