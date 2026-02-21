from __future__ import annotations
from optimization_system.models.modification import Modification, ModificationType
class ModificationPlanner:
    def plan_modification(self,opportunity):
        t=ModificationType.CAPABILITY_REPLACE if 'capability' in opportunity.title.lower() else ModificationType.SYSTEM_CONFIG_CHANGE
        return Modification(t,f'Apply {opportunity.title}',opportunity.description,opportunity.phase,opportunity.component,opportunity.component,'auto planned',before_state={'state':'before'},after_state={'state':'after'},rollback_data={'state':'before'})
    def plan_capability_replacement(self,old_id,new_id): return Modification(ModificationType.CAPABILITY_REPLACE,'Replace capability','replace','phase1','registry',old_id,f'{old_id}->{new_id}',before_state={'cap':old_id},after_state={'cap':new_id},rollback_data={'cap':old_id})
    def plan_strategy_replacement(self,old_name,new_name): return Modification(ModificationType.STRATEGY_REPLACE,'Replace strategy','replace','phase2','strategy_engine',old_name,f'{old_name}->{new_name}',before_state={'strategy':old_name},after_state={'strategy':new_name},rollback_data={'strategy':old_name})
    def plan_config_change(self,key,old_value,new_value): return Modification(ModificationType.SYSTEM_CONFIG_CHANGE,'Config change','config','system','config',key,f'{old_value}->{new_value}',before_state={key:old_value},after_state={key:new_value},rollback_data={key:old_value})
    def plan_capability_addition(self,capability_spec): return Modification(ModificationType.CAPABILITY_REGISTER,'Add capability','add','phase1','registry',capability_spec.get('name','new'),'register',before_state={},after_state=capability_spec,rollback_data={'remove':capability_spec.get('name','new')})
    def plan_capability_removal(self,capability_id): return Modification(ModificationType.CAPABILITY_DEACTIVATE,'Remove capability','remove','phase1','registry',capability_id,'deactivate',before_state={'active':True},after_state={'active':False},rollback_data={'active':True})
