from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from construction_system.utils.hash_utils import generate_id
@dataclass
class SandboxResult:
    result_id:str=field(default_factory=generate_id);sandbox_id:str='';code_executed:str='';execution_success:bool=False;stdout:str='';stderr:str='';return_value:object=None;exit_code:int=0;duration_ms:float=0.0;resource_usage:dict=field(default_factory=dict);security_violations:list[str]=field(default_factory=list);created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
