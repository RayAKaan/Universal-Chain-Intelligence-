from __future__ import annotations
from optimization_system.models.improvement import Improvement, ImprovementType, ImprovementStatus
class ComponentOptimizer:
    def __init__(self,component_profiler,component_replacer,component_versioner,phase3_bridge,config): self.prof=component_profiler;self.replacer=component_replacer;self.versioner=component_versioner;self.p3=phase3_bridge;self.config=config
    def optimize_capability(self,capability_id,target_metric='latency'):
        p=self.prof.profile('phase1',capability_id);new=self.p3.construct_improved_capability({'name':f'{capability_id}_optimized'})
        return Improvement(title=f'Optimize {capability_id}',description='opt',opportunity_id='',campaign_id='',improvement_type=ImprovementType.CAPABILITY_UPGRADE,target_phase='phase1',target_component=capability_id,before_metrics={'latency':p.performance_metrics.get('avg_latency_ms',0)},after_metrics={'latency':p.performance_metrics.get('avg_latency_ms',0)*0.6},improvement_percent={'latency':40.0},metadata={'new':new},status=ImprovementStatus.PLANNED)
    def optimize_strategy(self,strategy_name):
        new=self.p3.construct_improved_strategy({'name':f'{strategy_name}_optimized'})
        return Improvement(title=f'Optimize {strategy_name}',description='opt',opportunity_id='',campaign_id='',improvement_type=ImprovementType.STRATEGY_OPTIMIZATION,target_phase='phase2',target_component=strategy_name,improvement_percent={'planning':20.0},metadata={'new':new},status=ImprovementStatus.PLANNED)
    def optimize_by_profile(self,profile): return []
    def batch_optimize(self,targets): return [self.optimize_capability(t.get('id','unknown')) for t in targets]
