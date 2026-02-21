from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from construction_system.utils.hash_utils import generate_id
@dataclass
class ProvenanceRecord:
    record_id:str=field(default_factory=generate_id);artifact_id:str='';action:str='created';actor:str='construction_system';source_spec_id:str='';source_blueprint_id:str='';source_task_id:str='';parent_artifacts:list[str]=field(default_factory=list);child_artifacts:list[str]=field(default_factory=list);inputs_used:dict=field(default_factory=dict);template_used:str='';timestamp:datetime=field(default_factory=lambda:datetime.now(timezone.utc));environment:dict=field(default_factory=dict);verification:dict=field(default_factory=dict);metadata:dict=field(default_factory=dict)
