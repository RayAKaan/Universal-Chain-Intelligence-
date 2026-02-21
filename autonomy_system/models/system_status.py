from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

class SystemHealth(str, Enum): BOOTING='BOOTING'; INITIALIZING='INITIALIZING'; HEALTHY='HEALTHY'; DEGRADED='DEGRADED'; UNHEALTHY='UNHEALTHY'; HEALING='HEALING'; MAINTENANCE='MAINTENANCE'; SHUTTING_DOWN='SHUTTING_DOWN'; OFFLINE='OFFLINE'
@dataclass
class PhaseStatus: phase_name:str; status:str='healthy'; score:float=1.0; component_count:int=0; active_tasks:int=0; error_count:int=0; last_heartbeat:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
@dataclass
class ResourceStatus: cpu_percent:float=0.0; memory_percent:float=0.0; memory_used_mb:int=0; memory_total_mb:int=0; disk_percent:float=0.0; disk_used_gb:float=0.0; disk_total_gb:float=0.0; gpu_available:bool=False; gpu_percent:float=0.0; active_threads:int=0; active_processes:int=0
@dataclass
class CapabilityStatusSummary: total:int=0; active:int=0; healthy:int=0; degraded:int=0; failed:int=0; recently_added:int=0; recently_removed:int=0
@dataclass
class GoalStatusSummary: total_received:int=0; active:int=0; queued:int=0; completed:int=0; failed:int=0; success_rate:float=0.0; avg_completion_time_ms:float=0.0
@dataclass
class ImprovementStatusSummary: total_improvements:int=0; active_campaigns:int=0; pending_experiments:int=0; improvements_today:int=0; cumulative_improvement_percent:float=0.0
@dataclass
class SystemStatus:
    overall_status:SystemHealth=SystemHealth.BOOTING; overall_score:float=0.0
    status_id:str=field(default_factory=lambda:str(uuid4())); timestamp:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
    phase_status:dict=field(default_factory=dict); resource_status:ResourceStatus=field(default_factory=ResourceStatus)
    capability_status:CapabilityStatusSummary=field(default_factory=CapabilityStatusSummary)
    goal_status:GoalStatusSummary=field(default_factory=GoalStatusSummary)
    improvement_status:ImprovementStatusSummary=field(default_factory=ImprovementStatusSummary)
    autonomy_level:str='guided'; uptime_seconds:float=0.0; boot_time:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
    active_goals:list=field(default_factory=list); recent_events:list=field(default_factory=list); warnings:list=field(default_factory=list); metadata:dict=field(default_factory=dict)
