from __future__ import annotations
from dataclasses import dataclass, field
from construction_system.models.recursive_task import ResourceBudget
@dataclass
class RecursiveContext:
    root_task_id:str;current_depth:int=0;max_depth:int=10;task_stack:list[str]=field(default_factory=list);spec_history:list[str]=field(default_factory=list);shared_artifacts:dict=field(default_factory=dict);shared_components:dict=field(default_factory=dict);resource_budget:ResourceBudget=field(default_factory=ResourceBudget);resource_used:dict=field(default_factory=dict);variables:dict=field(default_factory=dict)
    def push(self,task_id,spec_id):self.task_stack.append(task_id);self.spec_history.append(spec_id);self.current_depth=len(self.task_stack)-1
    def pop(self):
        if self.task_stack:self.task_stack.pop();
        if self.spec_history:self.spec_history.pop();self.current_depth=max(0,len(self.task_stack)-1)
    def get_artifact(self,artifact_id):return self.shared_artifacts.get(artifact_id)
    def store_artifact(self,artifact):self.shared_artifacts[artifact.artifact_id]=artifact
    def get_component(self,component_id):return self.shared_components.get(component_id)
    def store_component(self,component):self.shared_components[component.component_id]=component
