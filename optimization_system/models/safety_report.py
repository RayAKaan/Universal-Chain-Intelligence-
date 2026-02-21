from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
@dataclass
class SafetyCheck: check_name:str; passed:bool; details:str=''; severity:str='low'
@dataclass
class SafetyReport:
    modification_id:str; is_safe:bool; risk_level:str='low'
    report_id:str=field(default_factory=lambda:str(uuid4()))
    checks_performed:list=field(default_factory=list); potential_impacts:list=field(default_factory=list)
    rollback_feasible:bool=True; rollback_complexity:str='simple'; recommendation:str='approve'
    reviewed_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); metadata:dict=field(default_factory=dict)
