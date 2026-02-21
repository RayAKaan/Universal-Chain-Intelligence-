from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
@dataclass
class RuleCondition: metric:str; operator:str; threshold:float; duration_seconds:float=0.0; context_filters:dict=field(default_factory=dict)
@dataclass
class RuleAction: action_type:str; parameters:dict=field(default_factory=dict); priority:int=1
@dataclass
class OptimizationRule:
    name:str; description:str; rule_type:str; condition:RuleCondition; action:RuleAction; confidence:float=0.8; source:str='manual'; enabled:bool=True
    rule_id:str=field(default_factory=lambda:str(uuid4()))
    trigger_count:int=0; last_triggered:datetime|None=None; created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); metadata:dict=field(default_factory=dict)
