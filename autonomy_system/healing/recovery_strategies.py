from __future__ import annotations
class BaseRecoveryStrategy:
    def can_handle(self,failure): return False
    def recover(self,failure): return True
    def estimate_recovery_time(self): return 1.0
class CapabilityRecoveryStrategy(BaseRecoveryStrategy):
    def can_handle(self,f): return f.get('failure_type')=='CAPABILITY_FAILURE'
class PhaseRecoveryStrategy(BaseRecoveryStrategy):
    def can_handle(self,f): return f.get('failure_type')=='PHASE_CRASH'
class ResourceRecoveryStrategy(BaseRecoveryStrategy):
    def can_handle(self,f): return f.get('failure_type')=='RESOURCE_EXHAUSTION'
class DatabaseRecoveryStrategy(BaseRecoveryStrategy):
    def can_handle(self,f): return f.get('failure_type')=='DATABASE_ERROR'
class ServiceRecoveryStrategy(BaseRecoveryStrategy):
    def can_handle(self,f): return f.get('failure_type') in {'NETWORK_FAILURE','UNKNOWN'}
class RecoveryStrategies:
    def __init__(self): self.strategies=[CapabilityRecoveryStrategy(),PhaseRecoveryStrategy(),ResourceRecoveryStrategy(),DatabaseRecoveryStrategy(),ServiceRecoveryStrategy()]
    def select(self,failure):
        for s in self.strategies:
            if s.can_handle(failure): return s
        return ServiceRecoveryStrategy()
