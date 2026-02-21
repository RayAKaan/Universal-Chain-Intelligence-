from __future__ import annotations
class GoalArbitrator:
    def arbitrate(self,goals,available_resources):
        return sorted(goals,key=lambda g:g.priority,reverse=True)
    def detect_conflicts(self,goal_a,goal_b): return goal_a.tenant_id==goal_b.tenant_id and 'exclusive' in (goal_a.metadata.get('mode','')+goal_b.metadata.get('mode',''))
    def can_execute_concurrently(self,goals): return all(not self.detect_conflicts(a,b) for i,a in enumerate(goals) for b in goals[i+1:])
