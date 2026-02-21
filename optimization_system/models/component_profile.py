from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
@dataclass
class ComponentProfile:
    phase:str; component_name:str; component_type:str
    profile_id:str=field(default_factory=lambda:str(uuid4()))
    performance_metrics:dict=field(default_factory=dict); resource_metrics:dict=field(default_factory=dict); usage_metrics:dict=field(default_factory=dict); quality_metrics:dict=field(default_factory=dict); trends:dict=field(default_factory=dict)
    profiled_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); sample_count:int=0; metadata:dict=field(default_factory=dict)
