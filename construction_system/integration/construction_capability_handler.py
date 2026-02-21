from __future__ import annotations
from execution_core.interfaces.execution_interface import ExecutionInterface
class ConstructionCapabilityHandler(ExecutionInterface):
    def __init__(self,construction_manager):self.cm=construction_manager
    def execute(self,payload):
        from construction_system.models.specification import Specification
        spec=Specification.from_dict(payload['specification']) if isinstance(payload.get('specification'),dict) else payload['specification']
        return self.cm.construct(spec).__dict__
    def validate(self,payload):
        if 'specification' not in payload: raise ValueError('specification required')
    def get_requirements(self):return {'threads':2}

def register_construction_capabilities(phase1_bridge):
    names=['construct_system','construct_pipeline','construct_capability','construct_strategy','construct_tool','construct_service','generate_code','validate_code','run_sandbox']
    ids=[]
    from construction_system.models.specification import Specification, SpecType
    for n in names:
        ids.append(phase1_bridge.register_constructed_capability(None,Specification(name=n,spec_type=SpecType.CAPABILITY_PLUGIN,description=n)))
    return ids
