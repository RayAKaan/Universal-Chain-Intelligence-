from __future__ import annotations
class GoalIsolator:
    def isolate(self,goal_record): return {'tenant_id':goal_record.tenant_id,'isolated':True}
