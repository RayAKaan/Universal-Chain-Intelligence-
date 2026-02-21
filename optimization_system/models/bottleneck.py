from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

class Severity(int, Enum): CRITICAL=0; HIGH=1; MEDIUM=2; LOW=3; INFO=4
class BottleneckType(str, Enum):
    SLOW_CAPABILITY='SLOW_CAPABILITY'; SLOW_PLANNING='SLOW_PLANNING'; SLOW_RESOLUTION='SLOW_RESOLUTION'; SLOW_EXECUTION='SLOW_EXECUTION'; SLOW_CONSTRUCTION='SLOW_CONSTRUCTION'; HIGH_FAILURE_RATE='HIGH_FAILURE_RATE'; HIGH_ERROR_RATE='HIGH_ERROR_RATE'; RESOURCE_CONTENTION='RESOURCE_CONTENTION'; RESOURCE_EXHAUSTION='RESOURCE_EXHAUSTION'; MEMORY_LEAK='MEMORY_LEAK'; QUEUE_BACKUP='QUEUE_BACKUP'; CAPABILITY_DEGRADATION='CAPABILITY_DEGRADATION'; STRATEGY_INEFFICIENCY='STRATEGY_INEFFICIENCY'; EXCESSIVE_RETRIES='EXCESSIVE_RETRIES'; TIMEOUT_FREQUENCY='TIMEOUT_FREQUENCY'; POOR_PARALLELISM='POOR_PARALLELISM'; DEPENDENCY_BOTTLENECK='DEPENDENCY_BOTTLENECK'; DISCOVERY_LAG='DISCOVERY_LAG'; STALE_CAPABILITIES='STALE_CAPABILITIES'; CUSTOM='CUSTOM'

@dataclass
class ImpactAssessment:
    affected_goals:int=0; affected_capabilities:int=0; performance_impact_percent:float=0.0; resource_waste_percent:float=0.0; description:str=''

@dataclass
class SuggestedAction:
    action_type:str; description:str; estimated_improvement_percent:float; estimated_effort:str='low'; priority:int=1

@dataclass
class Bottleneck:
    bottleneck_type:BottleneckType; severity:Severity; phase:str; component:str; description:str; metric_name:str; current_value:float; threshold_value:float; deviation_percent:float
    bottleneck_id:str=field(default_factory=lambda: str(uuid4()))
    impact:ImpactAssessment=field(default_factory=ImpactAssessment)
    suggested_actions:list=field(default_factory=list)
    first_detected:datetime=field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen:datetime=field(default_factory=lambda: datetime.now(timezone.utc))
    occurrence_count:int=1
    status:str='active'; resolution:str=''; metadata:dict=field(default_factory=dict)
