from __future__ import annotations

from planning_system.feedback.outcome_analyzer import analyze


class FeedbackEngine:
    def __init__(self, planning_memory, strategy_learner):
        self.planning_memory = planning_memory
        self.strategy_learner = strategy_learner

    def record_outcome(self, goal, plan, result):
        self.planning_memory.store_plan_outcome(goal, plan, result)
        ana = analyze(result)
        self.strategy_learner.update_strategy_scores(goal.goal_type, goal.intent.domain, plan.strategy_used, ana.success, {"duration": result.total_duration_ms})

    def get_recommendations(self, goal):
        best = self.strategy_learner.get_best_strategy(goal.goal_type, goal.intent.domain)
        sims = self.planning_memory.find_similar_goals(goal)
        return {
            "recommended_strategy": best,
            "known_pitfalls": ["timeouts on heavy steps"],
            "estimated_success_rate": 0.75,
            "suggested_capabilities": [s.get("goal_type") for s in sims],
        }
