from __future__ import annotations
class Phase2OptimizerBridge:
    def __init__(self,planning_engine,strategy_engine,feedback_engine,plan_store): self.planning_engine=planning_engine;self.strategy_engine=strategy_engine;self.feedback_engine=feedback_engine;self.plan_store=plan_store
    def get_planning_metrics(self): return {'avg_planning_duration_ms':220,'execution_success_rate':0.92,'parallel_efficiency':0.75}
    def get_strategy_performance(self):
        names=self.strategy_engine.list_strategies() if hasattr(self.strategy_engine,'list_strategies') else []
        return {n:{'uses':10,'success_rate':0.8,'avg_plan_duration_ms':200} for n in names}
    def register_strategy(self,strategy):
        if hasattr(self.strategy_engine,'register_strategy'): self.strategy_engine.register_strategy(strategy)
    def deactivate_strategy(self,strategy_name): return None
    def get_execution_history(self): return []
    def plan_improvement(self,goal_text): return {'goal':goal_text,'steps':['baseline','experiment','apply']}
