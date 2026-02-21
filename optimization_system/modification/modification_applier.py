from __future__ import annotations
from datetime import datetime, timezone
class ModificationApplier:
    def __init__(self,phase0_bridge=None,phase1_bridge=None,phase2_bridge=None): self.p0=phase0_bridge;self.p1=phase1_bridge;self.p2=phase2_bridge
    def apply(self,modification):
        modification.applied=True; modification.applied_at=datetime.now(timezone.utc)
        if modification.modification_type.value=='CAPABILITY_REPLACE' and self.p1:
            return self.p1.replace_capability(modification.before_state.get('cap',modification.target_identifier),modification.after_state.get('cap',modification.target_identifier))
        return True
