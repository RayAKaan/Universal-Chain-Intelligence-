from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from construction_system.utils.hash_utils import generate_id

class SpecType(str,Enum):
    FUNCTION='FUNCTION';CLASS='CLASS';MODULE='MODULE';PACKAGE='PACKAGE';PIPELINE='PIPELINE';SERVICE='SERVICE';API='API';CLI_TOOL='CLI_TOOL';CAPABILITY_PLUGIN='CAPABILITY_PLUGIN';STRATEGY_PLUGIN='STRATEGY_PLUGIN';DATA_PROCESSOR='DATA_PROCESSOR';TRANSFORMER='TRANSFORMER';COMPOSITE_SYSTEM='COMPOSITE_SYSTEM';CONFIGURATION='CONFIGURATION';DOCKERFILE='DOCKERFILE';SCRIPT='SCRIPT'
@dataclass
class SpecIO:name:str;data_type:str;description:str='';required:bool=True;default_value:Any=None;constraints:list[dict]=field(default_factory=list);format:str=''
@dataclass
class ComponentSpec:component_id:str;name:str;component_type:str;specification:dict;dependencies:list[str]=field(default_factory=list);config:dict=field(default_factory=dict)
@dataclass
class MethodSpec:method_name:str;parameters:list[dict]=field(default_factory=list);return_type:str='Any';description:str=''
@dataclass
class PropertySpec:name:str;type:str='Any';readable:bool=True;writable:bool=True
@dataclass
class InterfaceSpec:interface_id:str;name:str;methods:list[MethodSpec]=field(default_factory=list);properties:list[PropertySpec]=field(default_factory=list)
@dataclass
class BehaviorSpec:trigger:str;action:str;conditions:list[str]=field(default_factory=list)
@dataclass
class DependencySpec:name:str;version:str='';type:str='python_package';optional:bool=False
@dataclass
class Specification:
    spec_id:str=field(default_factory=generate_id);name:str='';version:str='1.0.0';spec_type:SpecType=SpecType.FUNCTION;description:str='';purpose:str='';inputs:list[SpecIO]=field(default_factory=list);outputs:list[SpecIO]=field(default_factory=list);components:list[ComponentSpec]=field(default_factory=list);interfaces:list[InterfaceSpec]=field(default_factory=list);behaviors:list[BehaviorSpec]=field(default_factory=list);constraints:list[dict]=field(default_factory=list);dependencies:list[DependencySpec]=field(default_factory=list);configuration:dict=field(default_factory=lambda:{'language':'python','target_directory':'constructed/','entry_point':'main.py','test_required':True,'sandbox_required':True});metadata:dict=field(default_factory=dict);created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc));updated_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
    def to_dict(self):
        d=asdict(self);d['spec_type']=self.spec_type.value;d['created_at']=self.created_at.isoformat();d['updated_at']=self.updated_at.isoformat();return d
    @classmethod
    def from_dict(cls,d):
        x=dict(d);x['spec_type']=SpecType(x.get('spec_type','FUNCTION'));x['inputs']=[SpecIO(**i) for i in x.get('inputs',[])];x['outputs']=[SpecIO(**i) for i in x.get('outputs',[])];x['components']=[ComponentSpec(**i) for i in x.get('components',[])];x['interfaces']=[InterfaceSpec(interface_id=i['interface_id'],name=i['name'],methods=[MethodSpec(**m) for m in i.get('methods',[])],properties=[PropertySpec(**p) for p in i.get('properties',[])]) for i in x.get('interfaces',[])];x['behaviors']=[BehaviorSpec(**i) for i in x.get('behaviors',[])];x['dependencies']=[DependencySpec(**i) for i in x.get('dependencies',[])];
        for k in ('created_at','updated_at'):
            if isinstance(x.get(k),str):
                from datetime import datetime
                x[k]=datetime.fromisoformat(x[k])
        return cls(**x)
