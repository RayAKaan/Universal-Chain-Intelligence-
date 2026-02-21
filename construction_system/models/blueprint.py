from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from construction_system.utils.hash_utils import generate_id
class BlueprintStatus(str,Enum):draft='draft';validated='validated';building='building';built='built';tested='tested';deployed='deployed';failed='failed'
@dataclass
class Blueprint:
    blueprint_id:str=field(default_factory=generate_id);spec_id:str='';name:str='';file_plan:list[dict]=field(default_factory=list);code_units:list=field(default_factory=list);directory_structure:list[str]=field(default_factory=list);build_order:list[str]=field(default_factory=list);dependency_install_commands:list[str]=field(default_factory=list);test_plan:dict=field(default_factory=lambda:{'test_files':[],'test_commands':[],'expected_outcomes':[]});integration_plan:dict=field(default_factory=lambda:{'register_as_capability':False,'capability_metadata':{},'register_as_strategy':False,'strategy_metadata':{},'auto_discover':True});estimated_lines_of_code:int=0;estimated_build_time_ms:float=0.0;status:BlueprintStatus=BlueprintStatus.draft;created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc));updated_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
