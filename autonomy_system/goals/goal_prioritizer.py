from __future__ import annotations
from autonomy_system.models.goal_record import GoalSource
class GoalPrioritizer:
    def prioritize(self,goal_record):
        p=goal_record.priority
        if goal_record.source in {GoalSource.EXTERNAL_API,GoalSource.EXTERNAL_CLI}: p+=10
        if 'urgent' in goal_record.raw_input.lower(): p+=20
        if len(goal_record.raw_input)<30: p+=5
        return max(0,min(100,p))
    def reprioritize_queue(self,queue):
        for g in queue: g.priority=self.prioritize(g)
        return sorted(queue,key=lambda x:x.priority,reverse=True)
