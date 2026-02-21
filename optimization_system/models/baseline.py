from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
@dataclass
class Baseline:
    name:str; metrics:dict
    baseline_id:str=field(default_factory=lambda:str(uuid4()))
    timestamp:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
    capability_performance:dict=field(default_factory=dict); strategy_performance:dict=field(default_factory=dict); metadata:dict=field(default_factory=dict)
