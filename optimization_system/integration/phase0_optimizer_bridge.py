from __future__ import annotations
from optimization_system.models.modification import Modification, ModificationType
class Phase0OptimizerBridge:
    def __init__(self,execution_engine,resource_manager,scheduler): self.execution_engine=execution_engine;self.resource_manager=resource_manager;self.scheduler=scheduler
    def get_execution_metrics(self): return {'avg_latency_ms':120,'success_rate':0.97,'queue_depth':4,'active_tasks':1}
    def get_resource_status(self): return {'threads':getattr(self.resource_manager,'max_workers',4),'queue_size':100,'timeout_ms':10000}
    def adjust_thread_pool(self,size): return Modification(ModificationType.RESOURCE_ALLOCATION_CHANGE,'Adjust thread pool','adjust','phase0','resource_manager','threads',f'{size}',after_state={'threads':size},rollback_data={'threads':self.get_resource_status().get('threads')})
    def adjust_queue_size(self,size): return Modification(ModificationType.RESOURCE_ALLOCATION_CHANGE,'Adjust queue size','adjust','phase0','scheduler','queue_size',f'{size}',after_state={'queue_size':size},rollback_data={'queue_size':self.get_resource_status().get('queue_size')})
    def adjust_timeout(self,timeout_ms): return Modification(ModificationType.SYSTEM_CONFIG_CHANGE,'Adjust timeout','adjust','phase0','execution_engine','timeout_ms',f'{timeout_ms}',after_state={'timeout_ms':timeout_ms},rollback_data={'timeout_ms':self.get_resource_status().get('timeout_ms')})
