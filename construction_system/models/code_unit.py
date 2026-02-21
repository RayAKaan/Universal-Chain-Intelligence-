from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from construction_system.utils.hash_utils import generate_id, hash_string
class CodeUnitType(str,Enum):FUNCTION='FUNCTION';CLASS='CLASS';METHOD='METHOD';STANDALONE_SCRIPT='STANDALONE_SCRIPT';MODULE_INIT='MODULE_INIT';CONFIGURATION='CONFIGURATION';CONSTANT_DEFINITION='CONSTANT_DEFINITION';IMPORT_BLOCK='IMPORT_BLOCK';DECORATOR='DECORATOR';CONTEXT_MANAGER='CONTEXT_MANAGER';DATA_CLASS='DATA_CLASS';ENUM_DEFINITION='ENUM_DEFINITION';EXCEPTION_CLASS='EXCEPTION_CLASS';TEST_CASE='TEST_CASE';TEST_FIXTURE='TEST_FIXTURE';MAIN_BLOCK='MAIN_BLOCK'
@dataclass
class CodeUnit:
    unit_id:str=field(default_factory=generate_id);name:str='';unit_type:CodeUnitType=CodeUnitType.FUNCTION;language:str='python';code:str='';imports:list[str]=field(default_factory=list);dependencies:list[str]=field(default_factory=list);input_parameters:list[dict]=field(default_factory=list);return_type:str='Any';docstring:str='';decorators:list[str]=field(default_factory=list);base_classes:list[str]=field(default_factory=list);is_test:bool=False;is_entry_point:bool=False;template_id:str='';template_variables:dict=field(default_factory=dict);validation_status:str='pending';validation_errors:list[str]=field(default_factory=list);source_spec_id:str='';created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc));checksum:str=''
    def __post_init__(self):
        if not self.checksum:self.checksum=hash_string(self.code or self.name)
