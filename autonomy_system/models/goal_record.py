from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
class GoalSource(str,Enum): EXTERNAL_CLI='EXTERNAL_CLI'; EXTERNAL_API='EXTERNAL_API'; EXTERNAL_FILE='EXTERNAL_FILE'; INTERNAL_GENERATED='INTERNAL_GENERATED'; INTERNAL_MAINTENANCE='INTERNAL_MAINTENANCE'; INTERNAL_IMPROVEMENT='INTERNAL_IMPROVEMENT'; INTERNAL_HEALING='INTERNAL_HEALING'; SCHEDULED='SCHEDULED'; TRIGGERED='TRIGGERED'
class GoalRecordStatus(str,Enum): RECEIVED='RECEIVED'; QUEUED='QUEUED'; INTERPRETING='INTERPRETING'; PLANNING='PLANNING'; EXECUTING='EXECUTING'; COMPLETED='COMPLETED'; FAILED='FAILED'; CANCELLED='CANCELLED'; PAUSED='PAUSED'; DEFERRED='DEFERRED'
@dataclass
class GoalRecord:
    source:GoalSource; raw_input:str; priority:int=50
    record_id:str=field(default_factory=lambda:str(uuid4())); goal_id:str=''; plan_id:str=''; status:GoalRecordStatus=GoalRecordStatus.RECEIVED
    result:any=None; error:str=''; submitted_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); started_at:datetime|None=None; completed_at:datetime|None=None
    execution_time_ms:float=0.0; planning_time_ms:float=0.0; resource_usage:dict=field(default_factory=dict)
    tenant_id:str='default'; feedback:dict=field(default_factory=dict); metadata:dict=field(default_factory=dict)
