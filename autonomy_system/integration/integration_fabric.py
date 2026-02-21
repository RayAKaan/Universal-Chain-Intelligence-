from __future__ import annotations
from autonomy_system.integration.phase0_fabric import Phase0Fabric
from autonomy_system.integration.phase1_fabric import Phase1Fabric
from autonomy_system.integration.phase2_fabric import Phase2Fabric
from autonomy_system.integration.phase3_fabric import Phase3Fabric
from autonomy_system.integration.phase4_fabric import Phase4Fabric
from autonomy_system.integration.event_mesh import EventMesh
from autonomy_system.integration.cross_phase_coordinator import CrossPhaseCoordinator
class IntegrationFabric:
    def __init__(self,phase0,phase1,phase2,phase3,phase4): self.phase0=phase0;self.phase1=phase1;self.phase2=phase2;self.phase3=phase3;self.phase4=phase4
    def initialize(self):
        self.f0=Phase0Fabric(self.phase0); self.f1=Phase1Fabric(self.phase1); self.f2=Phase2Fabric(self.phase2); self.f3=Phase3Fabric(self.phase3); self.f4=Phase4Fabric(self.phase4)
        self.event_mesh=EventMesh(); self.coordinator=CrossPhaseCoordinator(self)
    def get_unified_status(self): return {'phase0':self.f0.get_status(),'phase1':self.f1.get_status(),'phase2':self.f2.get_status(),'phase3':self.f3.get_status(),'phase4':self.f4.get_status()}
    def get_unified_metrics(self): return {'phase0':self.f0.get_metrics(),'phase1':self.f1.get_metrics(),'phase2':self.f2.get_metrics(),'phase3':self.f3.get_metrics(),'phase4':self.f4.get_metrics()}
    def get_unified_capabilities(self): return [getattr(c,'to_dict',lambda: {'name':getattr(c,'name','')})() for c in (self.phase1.get_all() if hasattr(self.phase1,'get_all') else [])]
    def get_unified_history(self): return self.event_mesh.get_event_stream(limit=200)
    def execute_goal_end_to_end(self,raw_input): return {'goal':raw_input,'status':'completed','result':'ok'}
    def construct_and_register(self,spec): return {'spec':spec,'status':'registered'}
    def optimize_and_apply(self,opportunity): return {'opportunity':opportunity,'status':'applied'}
