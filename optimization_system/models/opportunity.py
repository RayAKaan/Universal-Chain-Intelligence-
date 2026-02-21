from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

class OpportunityType(str, Enum):
    REPLACE_SLOW_CAPABILITY='REPLACE_SLOW_CAPABILITY'; UPGRADE_CAPABILITY='UPGRADE_CAPABILITY'; ADD_MISSING_CAPABILITY='ADD_MISSING_CAPABILITY'; PRUNE_UNUSED_CAPABILITY='PRUNE_UNUSED_CAPABILITY'; OPTIMIZE_PLANNING_STRATEGY='OPTIMIZE_PLANNING_STRATEGY'; CREATE_NEW_STRATEGY='CREATE_NEW_STRATEGY'; OPTIMIZE_RESOURCE_ALLOCATION='OPTIMIZE_RESOURCE_ALLOCATION'; IMPROVE_PARALLELISM='IMPROVE_PARALLELISM'; REDUCE_ERROR_RATE='REDUCE_ERROR_RATE'; ADD_CACHING='ADD_CACHING'; OPTIMIZE_EXECUTION_ORDER='OPTIMIZE_EXECUTION_ORDER'; REDUCE_REDUNDANCY='REDUCE_REDUNDANCY'; IMPROVE_FAILURE_HANDLING='IMPROVE_FAILURE_HANDLING'; OPTIMIZE_CONSTRUCTION_TEMPLATES='OPTIMIZE_CONSTRUCTION_TEMPLATES'; IMPROVE_RESOLUTION_ACCURACY='IMPROVE_RESOLUTION_ACCURACY'; REDUCE_PLANNING_OVERHEAD='REDUCE_PLANNING_OVERHEAD'; CONSOLIDATE_CAPABILITIES='CONSOLIDATE_CAPABILITIES'; CUSTOM='CUSTOM'

@dataclass
class Opportunity:
    opportunity_type:OpportunityType; title:str; description:str; phase:str; component:str; current_performance:dict; estimated_improvement:dict; implementation_approach:str
    estimated_effort:str='medium'; priority_score:float=0.0; prerequisites:list=field(default_factory=list); risks:list=field(default_factory=list)
    source:str='manual'; source_bottleneck_id:str=''; source_rule_id:str=''; status:str='identified'
    opportunity_id:str=field(default_factory=lambda: str(uuid4()))
    created_at:datetime=field(default_factory=lambda: datetime.now(timezone.utc)); updated_at:datetime=field(default_factory=lambda: datetime.now(timezone.utc)); metadata:dict=field(default_factory=dict)
