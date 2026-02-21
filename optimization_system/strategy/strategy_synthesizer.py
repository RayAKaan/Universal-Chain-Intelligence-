from __future__ import annotations
class StrategySynthesizer:
    def __init__(self,phase3_bridge): self.p3=phase3_bridge
    def synthesize_strategy(self,goal_type,optimization_target): return self.p3.construct_improved_strategy({'name':f'{goal_type}_{optimization_target}_strategy'})
    def combine_strategies(self,strategy_names,name): return self.p3.construct_improved_strategy({'name':name,'description':'hybrid'})
