from __future__ import annotations
class HistoryEndpoint:
    def __init__(self,core): self.core=core
    def get(self): return [g.__dict__ for g in self.core.goal_manager.get_history(100)]
