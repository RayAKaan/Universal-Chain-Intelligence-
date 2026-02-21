from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
class ModificationType(str,Enum): CAPABILITY_REGISTER='CAPABILITY_REGISTER'; CAPABILITY_DEACTIVATE='CAPABILITY_DEACTIVATE'; CAPABILITY_REPLACE='CAPABILITY_REPLACE'; CAPABILITY_CONFIG_CHANGE='CAPABILITY_CONFIG_CHANGE'; STRATEGY_REGISTER='STRATEGY_REGISTER'; STRATEGY_DEACTIVATE='STRATEGY_DEACTIVATE'; STRATEGY_REPLACE='STRATEGY_REPLACE'; RESOURCE_ALLOCATION_CHANGE='RESOURCE_ALLOCATION_CHANGE'; SYSTEM_CONFIG_CHANGE='SYSTEM_CONFIG_CHANGE'; TEMPLATE_UPDATE='TEMPLATE_UPDATE'; PRIORITY_ADJUSTMENT='PRIORITY_ADJUSTMENT'; THRESHOLD_ADJUSTMENT='THRESHOLD_ADJUSTMENT'; CUSTOM='CUSTOM'
@dataclass
class Modification:
    modification_type:ModificationType; title:str; description:str; target_phase:str; target_component:str; target_identifier:str; change_description:str
    modification_id:str=field(default_factory=lambda:str(uuid4()))
    before_state:dict=field(default_factory=dict); after_state:dict=field(default_factory=dict); safety_report:dict=field(default_factory=dict)
    experiment_id:str=''; improvement_id:str=''; applied:bool=False; applied_at:datetime|None=None; applied_by:str='optimization_system'
    rollback_available:bool=True; rollback_data:dict=field(default_factory=dict); rolled_back:bool=False; rolled_back_at:datetime|None=None
    verification_status:str='pending'; verification_results:dict=field(default_factory=dict); created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); metadata:dict=field(default_factory=dict)
