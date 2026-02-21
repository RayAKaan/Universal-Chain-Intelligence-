from optimization_system.component.optimization_strategies.base_optimization_strategy import BaseOptimizationStrategy
class ResourceOptimizerStrategy(BaseOptimizationStrategy):
    name='resource_optimizer_strategy';target_metric='resource_usage'
    def can_optimize(self,p): return p.resource_metrics.get('avg_cpu_percent',0)>70
    def optimize(self,p,context): return [{'action':'reduce_cpu'}] if self.can_optimize(p) else []
