from __future__ import annotations
from capability_system.models.capability import Capability, CapabilityType, CapabilityState, ExecutionType
class RegistrationError(Exception):pass
class Phase1ConstructorBridge:
    def __init__(self,capability_registry,lifecycle_manager,event_bus):self.registry=capability_registry;self.lifecycle=lifecycle_manager;self.event_bus=event_bus
    def register_constructed_capability(self,component,spec):
        cap=Capability(name=spec.name,version=spec.version,capability_type=CapabilityType.PYTHON_FUNCTION,category=spec.metadata.get('category','constructed'),subcategory=spec.metadata.get('subcategory','generated'),description=spec.description,execution_endpoint='builtins.print',execution_type=ExecutionType.PYTHON_FUNCTION,metadata={'source':'constructed','author':'construction_system','license':'','tags':['constructed'],'documentation_url':'','repository_url':''},state=CapabilityState.REGISTERED)
        cid=self.registry.register(cap);self.registry.activate(cid);return cid
    def update_constructed_capability(self,capability_id,component): self.registry.update(capability_id,{'description':component.name})
    def get_constructed_capabilities(self): return [c for c in self.registry.get_all() if c.metadata.get('source')=='constructed']
    def verify_capability_operational(self,capability_id): return self.registry.exists(capability_id)
