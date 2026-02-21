from __future__ import annotations
from optimization_system.models.modification import Modification, ModificationType
class CapabilityPruner:
    def __init__(self,phase1_bridge,config): self.p1=phase1_bridge;self.config=config
    def identify_candidates(self): return [cid for cid,p in self.p1.get_all_capability_performances().items() if p.get('days_since_used',0)>30]
    def prune(self,capability_id): return Modification(ModificationType.CAPABILITY_DEACTIVATE,'Prune capability','unused','phase1','registry',capability_id,'deactivate',before_state={'active':True},after_state={'active':False},rollback_data={'active':True})
    def safe_prune(self,candidates): return [self.prune(c) for c in candidates]
