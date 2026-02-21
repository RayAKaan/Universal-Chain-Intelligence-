from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from construction_system.utils.hash_utils import generate_id
class ComponentType(str,Enum):LIBRARY='LIBRARY';SERVICE='SERVICE';TOOL='TOOL';PIPELINE_STAGE='PIPELINE_STAGE';PLUGIN='PLUGIN';DATA_PROCESSOR='DATA_PROCESSOR';MODEL_WRAPPER='MODEL_WRAPPER';API_HANDLER='API_HANDLER';CLI_APPLICATION='CLI_APPLICATION';COMPOSITE='COMPOSITE'
class ComponentStatus(str,Enum):built='built';tested='tested';validated='validated';deployed='deployed';failed='failed'
@dataclass
class Component:
    component_id:str=field(default_factory=generate_id);name:str='';version:str='1.0.0';component_type:ComponentType=ComponentType.LIBRARY;blueprint_id:str='';spec_id:str='';files:list[str]=field(default_factory=list);entry_point:str='';provided_interfaces:list[dict]=field(default_factory=list);required_interfaces:list[dict]=field(default_factory=list);status:ComponentStatus=ComponentStatus.built;test_results:dict=field(default_factory=lambda:{'passed':0,'failed':0,'errors':0,'coverage':0.0});artifact_ids:list[str]=field(default_factory=list);created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc));built_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc));metadata:dict=field(default_factory=dict)
