from __future__ import annotations
class Phase1Fabric:
    def __init__(self,phase1): self.phase1=phase1
    def initialize(self): return None
    def health_check(self): return 'healthy'
    def get_metrics(self): return {'capabilities':len(self.phase1.get_all()) if hasattr(self.phase1,'get_all') else 0}
    def get_status(self): return {'status':'healthy'}
    def shutdown(self): return None
