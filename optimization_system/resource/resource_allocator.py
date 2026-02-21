from __future__ import annotations
from optimization_system.models.modification import Modification, ModificationType
class ResourceAllocator:
    def propose_reallocation(self,current,targets): return {k:targets.get(k,current.get(k)) for k in set(current)|set(targets)}
    def apply_reallocation(self,allocation): return Modification(ModificationType.RESOURCE_ALLOCATION_CHANGE,'Apply allocation','reallocation','phase0','resource_manager','allocation','apply',after_state=allocation,rollback_data={})
