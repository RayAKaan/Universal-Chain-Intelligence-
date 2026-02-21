from __future__ import annotations
from autonomy_system.models.goal_record import GoalRecord, GoalSource
class GoalGenerator:
    def __init__(self,performance_analyzer,bottleneck_detector,capability_registry,self_healer,config): self.pa=performance_analyzer;self.bd=bottleneck_detector;self.registry=capability_registry;self.healer=self_healer;self.config=config; self.generated=set()
    def should_generate(self,goal_type): return goal_type not in self.generated
    def _mk(self,text,source,priority,reason):
        r=GoalRecord(source=source,raw_input=text,priority=priority,metadata={'reason':reason}); return r
    def generate_maintenance_goals(self):
        return [self._mk('Benchmark all capabilities that have not been benchmarked in 24 hours',GoalSource.INTERNAL_MAINTENANCE,self.config.MAINTENANCE_GOAL_PRIORITY,'maintenance'),self._mk('Health check all active capabilities',GoalSource.INTERNAL_MAINTENANCE,self.config.MAINTENANCE_GOAL_PRIORITY,'maintenance')]
    def generate_improvement_goals(self):
        return [self._mk('Replace slow_processor with a faster alternative',GoalSource.INTERNAL_IMPROVEMENT,self.config.IMPROVEMENT_GOAL_PRIORITY,'bottleneck'),self._mk('Optimize resource allocation for peak efficiency',GoalSource.INTERNAL_IMPROVEMENT,self.config.IMPROVEMENT_GOAL_PRIORITY,'optimization')]
    def generate_healing_goals(self):
        return [self._mk('Restart failed capability api_caller',GoalSource.INTERNAL_HEALING,self.config.HEALING_GOAL_PRIORITY,'healing')]
    def generate_exploration_goals(self):
        return [self._mk('Discover new capabilities on the system',GoalSource.INTERNAL_GENERATED,self.config.EXPLORATION_GOAL_PRIORITY,'exploration')]
    def generate_goals(self):
        goals=self.generate_maintenance_goals()+self.generate_improvement_goals()+self.generate_healing_goals()+self.generate_exploration_goals()
        return goals[:self.config.MAX_GENERATED_GOALS_PER_CYCLE]
