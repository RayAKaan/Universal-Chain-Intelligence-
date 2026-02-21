from __future__ import annotations
class GoalCorrelator:
    def correlate(self,goals): return [goals] if goals else []
    def find_dependencies(self,goal,all_goals): return [g.record_id for g in all_goals if g.priority>goal.priority][:2]
    def find_similar(self,goal,history): return [h for h in history if goal.raw_input.split(' ')[0] in h.raw_input][:5]
