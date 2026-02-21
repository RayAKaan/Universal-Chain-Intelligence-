from __future__ import annotations

from capability_system.query.filters import apply_filters
from capability_system.query.ranking import rank_by_composite_score, rank_by_latency, rank_by_reliability


class QueryEngine:
    def __init__(self, registry):
        self.registry = registry

    def search(self, query: str):
        q = query.lower()
        out = []
        for c in self.registry.get_all():
            hay = " ".join([c.name, c.description, c.category, c.subcategory, " ".join(c.metadata.get("tags", []))]).lower()
            if q in hay:
                out.append(c)
        return out

    def filter(self, filters: dict):
        return apply_filters(self.registry.get_all(), filters)

    def rank(self, capabilities, criteria: str):
        if criteria == "latency":
            return rank_by_latency(capabilities)
        if criteria == "reliability":
            return rank_by_reliability(capabilities)
        return rank_by_composite_score(capabilities)

    def recommend(self, task_type: str, input_type: str, output_type: str):
        candidates = [
            c for c in self.registry.get_all()
            if task_type.lower() in c.category.lower() or task_type.lower() in c.subcategory.lower()
        ]
        return self.rank(candidates, "composite")[:10]

    def find_similar(self, capability_id: str):
        target = self.registry.get(capability_id)
        return [
            c for c in self.registry.get_all()
            if c.capability_id != capability_id and (c.capability_type == target.capability_type or c.category == target.category or bool(set(c.metadata.get("tags", [])) & set(target.metadata.get("tags", []))))
        ]
