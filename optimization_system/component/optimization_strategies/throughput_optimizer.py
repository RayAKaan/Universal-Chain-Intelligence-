from optimization_system.component.optimization_strategies.base_optimization_strategy import BaseOptimizationStrategy
class ThroughputOptimizer(BaseOptimizationStrategy):
    name='throughput_optimizer';target_metric='throughput'
    def can_optimize(self,p): return p.performance_metrics.get('throughput_per_second',0)<5
    def optimize(self,p,context): return [{'action':'parallelize'}] if self.can_optimize(p) else []
