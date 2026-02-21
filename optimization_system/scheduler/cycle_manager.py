from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
@dataclass
class CycleResult:
    cycle_id:str=field(default_factory=lambda:str(uuid4()))
    timestamp:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
    metrics_collected:int=0; bottlenecks_found:int=0; opportunities_found:int=0; campaigns_planned:int=0; improvements_applied:int=0; regressions_detected:int=0; duration_ms:float=0.0
class CycleManager:
    def __init__(self,engine): self.engine=engine
    def execute_cycle(self): return self.engine.run_improvement_cycle()
