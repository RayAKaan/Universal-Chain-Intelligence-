from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

class ImprovementType(str, Enum): CAPABILITY_REPLACEMENT='CAPABILITY_REPLACEMENT'; CAPABILITY_UPGRADE='CAPABILITY_UPGRADE'; CAPABILITY_ADDITION='CAPABILITY_ADDITION'; CAPABILITY_REMOVAL='CAPABILITY_REMOVAL'; STRATEGY_OPTIMIZATION='STRATEGY_OPTIMIZATION'; STRATEGY_CREATION='STRATEGY_CREATION'; STRATEGY_REPLACEMENT='STRATEGY_REPLACEMENT'; RESOURCE_REALLOCATION='RESOURCE_REALLOCATION'; CONFIGURATION_CHANGE='CONFIGURATION_CHANGE'; TEMPLATE_IMPROVEMENT='TEMPLATE_IMPROVEMENT'; EXECUTION_OPTIMIZATION='EXECUTION_OPTIMIZATION'; PLANNING_OPTIMIZATION='PLANNING_OPTIMIZATION'; CONSTRUCTION_OPTIMIZATION='CONSTRUCTION_OPTIMIZATION'; ARCHITECTURE_CHANGE='ARCHITECTURE_CHANGE'; CUSTOM='CUSTOM'
class ImprovementStatus(str, Enum): PROPOSED='PROPOSED'; PLANNED='PLANNED'; EXPERIMENTING='EXPERIMENTING'; EXPERIMENT_PASSED='EXPERIMENT_PASSED'; EXPERIMENT_FAILED='EXPERIMENT_FAILED'; APPLYING='APPLYING'; APPLIED='APPLIED'; VERIFYING='VERIFYING'; VERIFIED='VERIFIED'; ROLLED_BACK='ROLLED_BACK'; REJECTED='REJECTED'

@dataclass
class Improvement:
    title:str; description:str; opportunity_id:str; campaign_id:str; improvement_type:ImprovementType; target_phase:str; target_component:str
    improvement_id:str=field(default_factory=lambda: str(uuid4()))
    before_metrics:dict=field(default_factory=dict); after_metrics:dict=field(default_factory=dict); improvement_percent:dict=field(default_factory=dict)
    modification_id:str=''; experiment_id:str=''; status:ImprovementStatus=ImprovementStatus.PROPOSED
    applied_at:datetime|None=None; verified_at:datetime|None=None; rolled_back_at:datetime|None=None
    rollback_available:bool=True; rollback_data:dict=field(default_factory=dict)
    created_at:datetime=field(default_factory=lambda: datetime.now(timezone.utc)); metadata:dict=field(default_factory=dict)
