from optimization_system.component.optimization_strategies.base_optimization_strategy import BaseOptimizationStrategy
class LatencyOptimizer(BaseOptimizationStrategy):
    name='latency_optimizer';target_metric='latency'
    def can_optimize(self,p): return p.performance_metrics.get('avg_latency_ms',0)>200
    def optimize(self,p,context): return [{'action':'replace'},{'action':'cache'}] if self.can_optimize(p) else []
