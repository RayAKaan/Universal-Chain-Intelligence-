from __future__ import annotations
class GoalEndpoint:
    def __init__(self,core): self.core=core
    def post(self,text,priority=50): return self.core.submit_goal(text,priority=priority).__dict__
    def get(self,goal_id):
        r=self.core.goal_manager.get_status(goal_id)
        return r.__dict__ if r else {}
