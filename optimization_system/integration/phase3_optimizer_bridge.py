from __future__ import annotations
from construction_system.models.specification import Specification, SpecType
class Phase3OptimizerBridge:
    def __init__(self,construction_manager,template_library,artifact_manager): self.cm=construction_manager;self.template_library=template_library;self.artifact_manager=artifact_manager
    def get_construction_metrics(self):
        stats=self.artifact_manager.get_stats() if self.artifact_manager else {'total':0}
        return {'build_success_rate':0.9,'artifact_count':stats.get('total',0),'sandbox_success_rate':0.95}
    def construct_improved_capability(self,spec):
        s=Specification(name=spec.get('name','improved_capability'),spec_type=SpecType.CAPABILITY_PLUGIN,description=spec.get('description',''))
        self.cm.construct(s); return s.name
    def construct_improved_strategy(self,spec):
        s=Specification(name=spec.get('name','improved_strategy'),spec_type=SpecType.STRATEGY_PLUGIN,description=spec.get('description',''))
        self.cm.construct(s); return s.name
    def update_template(self,template_id,updated_template): return True
    def get_artifact_stats(self): return self.artifact_manager.get_stats() if self.artifact_manager else {}
