from optimization_system.component.optimization_strategies.base_optimization_strategy import BaseOptimizationStrategy
class ReliabilityOptimizer(BaseOptimizationStrategy):
    name='reliability_optimizer';target_metric='reliability'
    def can_optimize(self,p): return p.performance_metrics.get('success_rate',1.0)<0.9
    def optimize(self,p,context): return [{'action':'retry'},{'action':'fallback'}] if self.can_optimize(p) else []
