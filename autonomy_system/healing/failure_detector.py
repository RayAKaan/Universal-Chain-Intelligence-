from __future__ import annotations
class FailureDetector:
    def __init__(self,phase_coordinator=None): self.phase_coordinator=phase_coordinator
    def detect_phase_failures(self):
        if not self.phase_coordinator:return []
        return [{'failure_type':'PHASE_CRASH','phase':k,'component':k,'severity':'high'} for k,v in self.phase_coordinator.health_check_all().items() if v!='healthy']
    def detect_capability_failures(self): return []
    def detect_resource_failures(self): return []
    def detect_service_failures(self): return []
    def detect_all(self): return self.detect_phase_failures()+self.detect_capability_failures()+self.detect_resource_failures()+self.detect_service_failures()
