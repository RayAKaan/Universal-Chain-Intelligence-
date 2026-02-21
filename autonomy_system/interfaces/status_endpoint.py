from __future__ import annotations
class StatusEndpoint:
    def __init__(self,core): self.core=core
    def get(self): return self.core.get_status().__dict__
