from __future__ import annotations


class StrategyLearner:
    def __init__(self):
        self.stats = {}

    def update_strategy_scores(self, goal_type, domain, strategy, success, metrics):
        key = (str(goal_type), domain, strategy)
        s = self.stats.setdefault(key, {"runs": 0, "success": 0})
        s["runs"] += 1
        s["success"] += 1 if success else 0

    def get_best_strategy(self, goal_type, domain):
        candidates = [(k[2], v["success"] / v["runs"]) for k, v in self.stats.items() if k[0] == str(goal_type) and k[1] == domain and v["runs"] > 0]
        return sorted(candidates, key=lambda x: x[1], reverse=True)[0][0] if candidates else "adaptive"

    def get_strategy_stats(self):
        return {str(k): {"runs": v["runs"], "success_rate": (v["success"] / v["runs"] if v["runs"] else 0.0)} for k, v in self.stats.items()}
