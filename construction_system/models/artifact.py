from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from construction_system.utils.hash_utils import generate_id
class ArtifactType(str,Enum):SOURCE_CODE='SOURCE_CODE';TEST_CODE='TEST_CODE';CONFIGURATION='CONFIGURATION';DOCUMENTATION='DOCUMENTATION';BUILD_SCRIPT='BUILD_SCRIPT';DOCKERFILE='DOCKERFILE';DATA_FILE='DATA_FILE';MODEL_FILE='MODEL_FILE';BINARY='BINARY';LOG='LOG';REPORT='REPORT'
@dataclass
class Artifact:
    artifact_id:str=field(default_factory=generate_id);name:str='';artifact_type:ArtifactType=ArtifactType.SOURCE_CODE;file_path:str='';file_size_bytes:int=0;checksum:str='';source_blueprint_id:str='';source_spec_id:str='';source_component_id:str='';content_type:str='text/plain';is_executable:bool=False;is_entry_point:bool=False;created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc));created_by:str='construction_system';provenance_id:str='';metadata:dict=field(default_factory=dict);tags:list[str]=field(default_factory=list)
