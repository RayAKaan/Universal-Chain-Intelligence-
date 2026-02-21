from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
class AcquisitionType(str,Enum): PYTHON_PACKAGE='PYTHON_PACKAGE'; SYSTEM_TOOL='SYSTEM_TOOL'; MODEL_DOWNLOAD='MODEL_DOWNLOAD'; API_INTEGRATION='API_INTEGRATION'; PLUGIN_INSTALL='PLUGIN_INSTALL'; CAPABILITY_CONSTRUCTION='CAPABILITY_CONSTRUCTION'
class AcquisitionStatus(str,Enum): REQUESTED='REQUESTED'; APPROVED='APPROVED'; DOWNLOADING='DOWNLOADING'; INSTALLING='INSTALLING'; TESTING='TESTING'; REGISTERED='REGISTERED'; FAILED='FAILED'; REJECTED='REJECTED'
@dataclass
class AcquisitionRecord:
    acquisition_type:AcquisitionType; name:str; reason:str; requested_by:str='system'
    acquisition_id:str=field(default_factory=lambda:str(uuid4())); version:str=''; source_url:str=''; source_type:str=''
    status:AcquisitionStatus=AcquisitionStatus.REQUESTED; safety_check_passed:bool=False; safety_report:dict=field(default_factory=dict); capability_id:str=''
    started_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); completed_at:datetime|None=None; metadata:dict=field(default_factory=dict)
