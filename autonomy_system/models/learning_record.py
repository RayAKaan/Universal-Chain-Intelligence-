from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
class LearningType(str,Enum): GOAL_OUTCOME='GOAL_OUTCOME'; CAPABILITY_PERFORMANCE='CAPABILITY_PERFORMANCE'; STRATEGY_EFFECTIVENESS='STRATEGY_EFFECTIVENESS'; FAILURE_PATTERN='FAILURE_PATTERN'; RESOURCE_PATTERN='RESOURCE_PATTERN'; USER_PREFERENCE='USER_PREFERENCE'; OPTIMIZATION_RESULT='OPTIMIZATION_RESULT'; ACQUISITION_OUTCOME='ACQUISITION_OUTCOME'
@dataclass
class LearningRecord:
    learning_type:LearningType; observation:dict; lesson:str; confidence:float
    record_id:str=field(default_factory=lambda:str(uuid4())); applicable_to:list=field(default_factory=list); created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); applied_count:int=0; last_applied:datetime|None=None
