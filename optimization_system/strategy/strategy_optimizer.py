from __future__ import annotations
from optimization_system.models.improvement import Improvement, ImprovementType, ImprovementStatus
class StrategyOptimizer:
    def __init__(self,strategy_evaluator,strategy_synthesizer,phase2_bridge,phase3_bridge,config): self.eval=strategy_evaluator;self.syn=strategy_synthesizer;self.p2=phase2_bridge;self.p3=phase3_bridge;self.config=config
    def optimize_strategy(self,strategy_name):
        new=self.syn.synthesize_strategy('general','speed')
        return Improvement(title=f'Optimize {strategy_name}',description='optimize strategy',opportunity_id='',campaign_id='',improvement_type=ImprovementType.STRATEGY_OPTIMIZATION,target_phase='phase2',target_component=strategy_name,status=ImprovementStatus.PLANNED,metadata={'new':new})
    def optimize_all(self): return [self.optimize_strategy(k) for k,v in self.eval.evaluate_all().items() if v['overall_score']<0.7]
