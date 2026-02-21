from __future__ import annotations
class Phase2ConstructorBridge:
    def __init__(self,strategy_engine,planning_engine):self.strategy_engine=strategy_engine;self.planning_engine=planning_engine
    def register_constructed_strategy(self,component,spec):
        from planning_system.strategies.base_strategy import BaseStrategy
        class Constructed(BaseStrategy):
            name=spec.name;description=spec.description or spec.name
            def plan(self,goal,context):return self._fallback(goal,context) if hasattr(self,'_fallback') else None
            def is_suitable(self,goal,context):return 0.5
        self.strategy_engine.register_strategy(Constructed());return spec.name
    def convert_spec_to_goal(self,spec):
        from planning_system.models.goal import Goal, Intent
        return Goal(raw_input=f'Build {spec.name}',title=f'Build {spec.name}',description=spec.description,intent=Intent(action='build',target=spec.name,domain=spec.metadata.get('domain','system'),qualifiers=[]))
    def plan_construction(self,spec):
        goal=self.convert_spec_to_goal(spec)
        strategy=self.strategy_engine.select_strategy(goal,None)
        return strategy.plan(goal,None)
