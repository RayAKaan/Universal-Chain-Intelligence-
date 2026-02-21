from __future__ import annotations
from abc import ABC, abstractmethod
class ConstructionError(Exception):pass
class BaseConstructor(ABC):
    constructor_name='base';supported_spec_types=[]
    def can_construct(self,spec): return spec.spec_type in self.supported_spec_types
    def estimate_build_time(self,spec): return 1000.0*max(1,len(spec.components))
    def validate_spec(self,spec):
        issues=[]
        if spec.spec_type not in self.supported_spec_types: issues.append('unsupported spec type')
        return issues
    @abstractmethod
    def construct(self,spec,context):...
