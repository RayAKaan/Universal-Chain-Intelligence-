from __future__ import annotations
from optimization_system.models.improvement import Improvement, ImprovementType, ImprovementStatus
class CapabilityEvolver:
    def __init__(self,capability_registry,capability_ranker,phase3_bridge,experiment_framework,config): self.registry=capability_registry;self.ranker=capability_ranker;self.p3=phase3_bridge;self.exp=experiment_framework;self.config=config
    def construct_improved_capability(self,capability_id,target_improvements): return self.p3.construct_improved_capability({'name':f'{capability_id}_evolved'})
    def replace_capability(self,old_id,new_id):
        from optimization_system.modification.modification_planner import ModificationPlanner
        return ModificationPlanner().plan_capability_replacement(old_id,new_id)
    def upgrade_capability(self,capability_id):
        new=self.construct_improved_capability(capability_id,{})
        return Improvement(title=f'Upgrade {capability_id}',description='evolve',opportunity_id='',campaign_id='',improvement_type=ImprovementType.CAPABILITY_UPGRADE,target_phase='phase1',target_component=capability_id,status=ImprovementStatus.PLANNED,metadata={'new':new})
    def evolve(self): return [self.upgrade_capability(cid) for cid in self.ranker.identify_underperformers(0.5)]
