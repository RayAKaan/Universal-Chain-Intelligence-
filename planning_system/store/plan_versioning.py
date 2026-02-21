from __future__ import annotations


class PlanVersioning:
    def __init__(self, plan_store):
        self.store = plan_store

    def create_version(self, plan):
        prev = self.get_latest_version(plan.plan_id)
        plan.version = (prev.get("version", 0) + 1) if isinstance(prev, dict) else plan.version + 1
        return plan

    def get_version(self, plan_id, version):
        for p in self.store.load_by_goal(plan_id):
            if p.get("version") == version:
                return p
        return None

    def get_all_versions(self, plan_id):
        return self.store.load_by_goal(plan_id)

    def get_latest_version(self, plan_id):
        rows = self.store.load_by_goal(plan_id)
        return sorted(rows, key=lambda x: x.get("version", 0))[-1] if rows else None

    def diff(self, plan_v1, plan_v2):
        return {
            "version_from": plan_v1.get("version"),
            "version_to": plan_v2.get("version"),
            "steps_delta": len(plan_v2.get("steps", [])) - len(plan_v1.get("steps", [])),
            "strategy_changed": plan_v1.get("strategy_used") != plan_v2.get("strategy_used"),
        }
