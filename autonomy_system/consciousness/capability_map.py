from __future__ import annotations
class CapabilityMap:
    def __init__(self,phase1_registry=None): self.registry=phase1_registry
    def build_map(self):
        caps=self.registry.get_all() if self.registry and hasattr(self.registry,'get_all') else []
        return {'all':[getattr(c,'name','') for c in caps]}
    def get_coverage(self):
        m=self.build_map(); return {'count':len(m['all']),'domains':{'general':len(m['all'])}}
    def get_gaps(self): return ['time-series forecasting','advanced visualization']
    def visualize_map(self): return '\n'.join(self.build_map()['all']) or 'No capabilities'
