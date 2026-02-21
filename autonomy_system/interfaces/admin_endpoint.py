from __future__ import annotations
class AdminEndpoint:
    def __init__(self,core): self.core=core
    def set_autonomy(self,level): self.core.set_autonomy_level(level); return {'ok':True}
    def shutdown(self): self.core.shutdown(); return {'ok':True}
