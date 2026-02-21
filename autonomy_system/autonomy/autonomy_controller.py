from __future__ import annotations
from autonomy_system.models.autonomy_state import AutonomyState, AutonomyLevel
from autonomy_system.autonomy.autonomy_levels import LEVEL_PERMISSIONS
from autonomy_system.autonomy.oversight_manager import OversightManager
from autonomy_system.autonomy.decision_authority import DecisionAuthority, ApprovalResult
class AutonomyController:
    def __init__(self,config,system_state,safety_governor):
        self.config=config; self.system_state=system_state; self.safety_governor=safety_governor; self.state=AutonomyState(autonomy_level=AutonomyLevel.GUIDED,permissions=LEVEL_PERMISSIONS[AutonomyLevel.GUIDED]); self.oversight=OversightManager(); self.authority=DecisionAuthority()
    def set_level(self,level):
        lv=AutonomyLevel[level.upper()] if isinstance(level,str) else level
        self.state.autonomy_level=lv; self.state.permissions=LEVEL_PERMISSIONS[lv]
    def get_level(self): return self.state.autonomy_level
    def get_permissions(self): return self.state.permissions
    def can_perform(self,action):
        p=self.state.permissions
        return {'execute_goal':p.can_execute_goals,'acquire_capability':p.can_acquire_capabilities,'modify_self':p.can_modify_self,'generate_goal':p.can_generate_goals,'prune_capability':p.can_prune_capabilities,'replace_strategy':p.can_replace_strategies,'allocate_resources':p.can_allocate_resources,'access_network':p.can_access_network}.get(action,False)
    def request_approval(self,action,details):
        res=self.authority.decide(action,details,self.state.autonomy_level,details.get('safety_report'))
        self.oversight.record_decision(action,self.state.autonomy_level,res.approved,{'reason':res.reason})
        return res
    def escalate(self,action,reason): self.oversight.record_decision(action,self.state.autonomy_level,False,{'reason':reason,'escalated':True})
    def get_state(self): return self.state
    def get_decision_log(self): return self.oversight.get_decisions()
