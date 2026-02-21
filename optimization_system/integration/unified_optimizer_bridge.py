from __future__ import annotations
class UnifiedOptimizerBridge:
    def __init__(self,phase0_bridge,phase1_bridge,phase2_bridge,phase3_bridge): self.p0=phase0_bridge;self.p1=phase1_bridge;self.p2=phase2_bridge;self.p3=phase3_bridge
    def get_system_wide_metrics(self): return {'phase0':self.p0.get_execution_metrics(),'phase1':self.p1.get_capability_metrics(),'phase2':self.p2.get_planning_metrics(),'phase3':self.p3.get_construction_metrics()}
    def get_system_health(self): return {'healthy':True,'metrics':self.get_system_wide_metrics()}
    def get_improvement_opportunities(self): return []
    def execute_improvement(self,improvement): return True
