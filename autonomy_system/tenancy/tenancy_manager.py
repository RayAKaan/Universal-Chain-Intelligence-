from __future__ import annotations
class TenancyManager:
    def __init__(self,goal_isolator,resource_partitioner,context_separator): self.goal_isolator=goal_isolator; self.resource_partitioner=resource_partitioner; self.context_separator=context_separator
    def isolate_goal(self,goal_record): return self.goal_isolator.isolate(goal_record)
