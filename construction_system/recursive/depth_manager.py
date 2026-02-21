from __future__ import annotations
class DepthManager:
    def __init__(self):self.current={};self.max_seen={}
    def track_depth(self,root_task_id,current_depth):self.current[root_task_id]=current_depth;self.max_seen[root_task_id]=max(current_depth,self.max_seen.get(root_task_id,0))
    def get_current_depth(self,root_task_id):return self.current.get(root_task_id,0)
    def get_max_depth_seen(self,root_task_id):return self.max_seen.get(root_task_id,0)
    def is_depth_safe(self,current_depth):return current_depth<=10
    def estimate_remaining_capacity(self,task):return {'remaining_depth':task.max_depth-task.depth,'remaining_children':task.resource_budget.max_child_tasks-len(task.child_task_ids)}
