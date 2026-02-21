from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from uuid import uuid4
class AutonomyLevel(IntEnum): PASSIVE=0; SUPERVISED=1; GUIDED=2; AUTONOMOUS=3; FULL_AUTONOMY=4
@dataclass
class AutonomyPermissions:
    can_execute_goals:bool; can_acquire_capabilities:bool; can_modify_self:bool; can_generate_goals:bool; can_prune_capabilities:bool; can_replace_strategies:bool; can_allocate_resources:bool; can_access_network:bool; max_concurrent_goals:int; max_resource_percent:float; require_approval_for:list
@dataclass
class AutonomyState:
    autonomy_level:AutonomyLevel=AutonomyLevel.GUIDED
    state_id:str=field(default_factory=lambda:str(uuid4())); timestamp:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
    permissions:AutonomyPermissions|None=None; active_constraints:list=field(default_factory=list)
    human_override_active:bool=False; last_human_interaction:datetime|None=None
    decisions_made:int=0; decisions_requiring_approval:int=0; decisions_auto_approved:int=0; decisions_rejected:int=0
