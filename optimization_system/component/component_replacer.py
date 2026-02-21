from __future__ import annotations
from optimization_system.models.modification import Modification, ModificationType
class ComponentReplacer:
    def plan_replacement(self,current_id,replacement_id,phase):
        t=ModificationType.CAPABILITY_REPLACE if phase=='phase1' else ModificationType.STRATEGY_REPLACE
        return Modification(t,'Replace component','replace',phase,'component',current_id,f'{current_id}->{replacement_id}',before_state={'id':current_id},after_state={'id':replacement_id},rollback_data={'id':current_id})
    def execute_replacement(self,modification): modification.applied=True; return True
    def rollback_replacement(self,modification): modification.rolled_back=True; return True
