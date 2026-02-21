from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
@dataclass
class TelemetryPoint:
    category:str; name:str; value:float; unit:str=''
    point_id:str=field(default_factory=lambda:str(uuid4())); timestamp:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); dimensions:dict=field(default_factory=dict); source_phase:str='system'; source_component:str='core'
