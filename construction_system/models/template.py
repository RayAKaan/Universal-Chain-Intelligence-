from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from construction_system.utils.hash_utils import generate_id
@dataclass
class Template:
    template_id:str=field(default_factory=generate_id);name:str='';description:str='';template_type:str='';language:str='python';template_string:str='';variables:list[dict]=field(default_factory=list);output_type:str='FUNCTION';tags:list[str]=field(default_factory=list);category:str='';examples:list[dict]=field(default_factory=list);created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc));version:str='1.0.0'
