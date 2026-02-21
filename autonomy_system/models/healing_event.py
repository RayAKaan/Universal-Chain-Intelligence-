from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
class FailureType(str,Enum): CAPABILITY_FAILURE='CAPABILITY_FAILURE'; EXECUTION_FAILURE='EXECUTION_FAILURE'; RESOURCE_EXHAUSTION='RESOURCE_EXHAUSTION'; DATABASE_ERROR='DATABASE_ERROR'; NETWORK_FAILURE='NETWORK_FAILURE'; PHASE_CRASH='PHASE_CRASH'; DEADLOCK='DEADLOCK'; MEMORY_LEAK='MEMORY_LEAK'; CORRUPTION='CORRUPTION'; UNKNOWN='UNKNOWN'
@dataclass
class HealingEvent:
    failure_type:FailureType; affected_phase:str; affected_component:str; severity:str
    event_id:str=field(default_factory=lambda:str(uuid4())); detection_method:str='monitor'; detection_time:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); recovery_strategy:str=''; recovery_actions:list=field(default_factory=list); recovery_time:datetime|None=None; recovery_success:bool=False; root_cause:str=''; prevention_rule:str=''; metadata:dict=field(default_factory=dict)
