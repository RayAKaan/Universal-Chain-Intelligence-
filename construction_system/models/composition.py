from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from construction_system.utils.hash_utils import generate_id
@dataclass
class Composition:
    composition_id:str=field(default_factory=generate_id);name:str='';components:list[str]=field(default_factory=list);wirings:list[dict]=field(default_factory=list);entry_points:list[dict]=field(default_factory=list);initialization_order:list[str]=field(default_factory=list);status:str='draft';created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
