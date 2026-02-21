from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
@dataclass
class RuntimeState:
    state_id:str=field(default_factory=lambda:str(uuid4())); pid:int=0; hostname:str='localhost'; boot_time:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); uptime_seconds:float=0.0; status:str='BOOTING'; autonomy_level:str='guided'; active_goals:int=0; queued_goals:int=0; completed_goals:int=0; total_capabilities:int=0; active_capabilities:int=0; improvement_cycles_completed:int=0; last_health_check:datetime|None=None; last_improvement_cycle:datetime|None=None; last_discovery_scan:datetime|None=None; errors_since_boot:int=0; healings_since_boot:int=0; memory_usage_mb:float=0.0; cpu_usage_percent:float=0.0
