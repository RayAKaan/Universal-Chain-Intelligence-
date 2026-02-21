from __future__ import annotations
from autonomy_system.models.system_status import SystemHealth
class LifecycleManager:
    def __init__(self): self.history=[]
    def get_valid_transitions(self,current):
        m={SystemHealth.BOOTING:[SystemHealth.INITIALIZING],SystemHealth.INITIALIZING:[SystemHealth.HEALTHY],SystemHealth.HEALTHY:[SystemHealth.DEGRADED,SystemHealth.MAINTENANCE,SystemHealth.SHUTTING_DOWN],SystemHealth.DEGRADED:[SystemHealth.UNHEALTHY,SystemHealth.HEALING,SystemHealth.HEALTHY],SystemHealth.UNHEALTHY:[SystemHealth.HEALING,SystemHealth.SHUTTING_DOWN],SystemHealth.HEALING:[SystemHealth.DEGRADED,SystemHealth.HEALTHY],SystemHealth.MAINTENANCE:[SystemHealth.HEALTHY],SystemHealth.SHUTTING_DOWN:[SystemHealth.OFFLINE]}
        return m.get(current,[])
    def manage_lifecycle_transition(self,from_state,to_state):
        if to_state not in self.get_valid_transitions(from_state) and to_state!=SystemHealth.SHUTTING_DOWN: return False
        self.history.append({'from':from_state.value,'to':to_state.value}); return True
    def get_transition_history(self): return self.history
