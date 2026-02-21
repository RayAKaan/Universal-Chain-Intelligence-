from __future__ import annotations


class ExecutionHistory:
    def __init__(self):
        self._results = []

    def record_execution(self, plan_id, result):
        self._results.append(result)

    def get_history(self, limit=100):
        return self._results[-limit:]

    def get_history_by_goal_type(self, goal_type):
        return [r for r in self._results if r.feedback.get("goal_type") == goal_type]

    def get_success_rate(self, goal_type=None):
        items = self.get_history_by_goal_type(goal_type) if goal_type else self._results
        if not items:
            return 0.0
        return len([r for r in items if r.status == "success"]) / len(items)

    def get_average_duration(self, goal_type=None):
        items = self.get_history_by_goal_type(goal_type) if goal_type else self._results
        if not items:
            return 0.0
        return sum(r.total_duration_ms for r in items) / len(items)
