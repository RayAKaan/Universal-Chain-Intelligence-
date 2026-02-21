from __future__ import annotations
class CapabilityEndpoint:
    def __init__(self,core): self.core=core
    def get(self): return self.core.get_capabilities()
