from __future__ import annotations
class UnifiedAPI:
    def __init__(self,core): self.core=core
    def submit_goal(self,text,priority=50): return self.core.submit_goal(text,priority=priority).__dict__
    def status(self): return self.core.get_status().__dict__
