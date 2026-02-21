from __future__ import annotations
from collections import defaultdict
from construction_system.config import MAX_RECURSION_DEPTH, MAX_TOTAL_RECURSIVE_TASKS
class RecursionLimitError(Exception):pass
class CycleDetectedError(Exception):pass
class RecursionController:
    def __init__(self,config):self.config=config;self.tasks=defaultdict(dict)
    def can_recurse(self,task):
        if task.depth>=task.max_depth: return False,'depth limit exceeded'
        if len(self.tasks[task.root_task_id])>=self.config.MAX_TOTAL_RECURSIVE_TASKS: return False,'task count limit exceeded'
        if task.resource_budget.max_child_tasks<=len(task.child_task_ids): return False,'child task budget exceeded'
        return True,''
    def allocate_budget(self,parent,num_children):
        b=parent.resource_budget
        n=max(1,num_children)
        budgets=[]
        for _ in range(n):
            from construction_system.models.recursive_task import ResourceBudget
            budgets.append(ResourceBudget(max_cpu_seconds=b.max_cpu_seconds/n,max_memory_mb=max(64,b.max_memory_mb//n),max_disk_mb=max(10,b.max_disk_mb//n),max_files=max(5,b.max_files//n),max_lines_of_code=max(100,b.max_lines_of_code//n),max_child_tasks=max(1,b.max_child_tasks//n)))
        return budgets
    def check_cycle(self,task,spec):
        seen=[t['spec_id'] for t in self.tasks[task.root_task_id].values()]
        return spec.spec_id in seen
    def get_depth_limit(self):return self.config.MAX_RECURSION_DEPTH
    def set_depth_limit(self,limit):self.config.MAX_RECURSION_DEPTH=limit
    def get_total_tasks_spawned(self,root_task_id):return len(self.tasks[root_task_id])
    def get_max_depth_reached(self,root_task_id):
        vals=[v['depth'] for v in self.tasks[root_task_id].values()]
        return max(vals) if vals else 0
    def record_task(self,task):self.tasks[task.root_task_id][task.task_id]={'parent':task.parent_task_id,'depth':task.depth,'spec_id':task.specification.spec_id if task.specification else ''}
    def get_task_tree(self,root_task_id):return self.tasks[root_task_id]
