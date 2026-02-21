from __future__ import annotations
from construction_system.models.specification import Specification, SpecType, SpecIO, ComponentSpec

class FunctionSpecBuilder:
    def __init__(self,name): self.s=Specification(name=name,spec_type=SpecType.FUNCTION)
    def with_parameter(self,name,type,required=True,default=None): self.s.inputs.append(SpecIO(name=name,data_type=type,required=required,default_value=default));return self
    def returns(self,type): self.s.outputs=[SpecIO(name='result',data_type=type)];return self
    def with_body(self,lines): self.s.metadata['body_lines']=lines;return self
    def with_docstring(self,doc): self.s.description=doc;return self
    def with_decorator(self,decorator): self.s.metadata.setdefault('decorators',[]).append(decorator);return self
    def async_(self): self.s.metadata['is_async']=True;return self
    def build(self): return self.s
class ClassSpecBuilder:
    def __init__(self,name): self.s=Specification(name=name,spec_type=SpecType.CLASS)
    def extends(self,b): self.s.metadata.setdefault('base_classes',[]).append(b);return self
    def with_init(self,params): self.s.metadata['init_params']=params;return self
    def with_method(self,name,params,return_type,body): self.s.behaviors.append(type('B',(),{'trigger':name,'action':'\n'.join(body),'conditions':[]})()); self.s.metadata.setdefault('methods',[]).append({'name':name,'params':params,'return_type':return_type,'body':body}); return self
    def with_property(self,name,type,getter,setter): self.s.metadata.setdefault('properties',[]).append({'name':name,'type':type,'getter':getter,'setter':setter});return self
    def with_class_variable(self,name,type,value): self.s.metadata.setdefault('class_variables',[]).append({'name':name,'type':type,'value':value});return self
    def with_docstring(self,doc): self.s.description=doc;return self
    def build(self): return self.s
class PipelineSpecBuilder:
    def __init__(self,name): self.s=Specification(name=name,spec_type=SpecType.PIPELINE)
    def with_stage(self,name,input_type,output_type,processing): self.s.components.append(ComponentSpec(component_id=name,name=name,component_type='MODULE',specification={'input_type':input_type,'output_type':output_type,'processing':processing}));return self
    def with_config(self,config): self.s.configuration.update(config);return self
    def parallel_stages(self,stage_names): self.s.metadata['parallel_stages']=stage_names;return self
    def build(self): return self.s
class SystemSpecBuilder:
    def __init__(self,name): self.s=Specification(name=name,spec_type=SpecType.COMPOSITE_SYSTEM)
    def with_component(self,name,spec): self.s.components.append(ComponentSpec(component_id=name,name=name,component_type=spec.spec_type.value,specification=spec.to_dict()));return self
    def with_interface(self,interface_spec): self.s.interfaces.append(interface_spec);return self
    def with_dependency(self,dep): self.s.dependencies.append(dep);return self
    def with_config(self,config): self.s.configuration.update(config);return self
    def build(self): return self.s
class CapabilitySpecBuilder(SystemSpecBuilder):
    def __init__(self,name): self.s=Specification(name=name,spec_type=SpecType.CAPABILITY_PLUGIN)
    def with_capability_type(self,type): self.s.metadata['capability_type']=type;return self
    def with_input_schema(self,schema): self.s.metadata['input_schema']=schema;return self
    def with_output_schema(self,schema): self.s.metadata['output_schema']=schema;return self
    def with_processing(self,logic): self.s.metadata['processing_logic']=logic;return self
    def with_category(self,category,subcategory): self.s.metadata['category']=category;self.s.metadata['subcategory']=subcategory;return self
class StrategySpecBuilder(SystemSpecBuilder):
    def __init__(self,name): self.s=Specification(name=name,spec_type=SpecType.STRATEGY_PLUGIN)
    def with_suitability(self,criteria): self.s.metadata['suitability']=criteria;return self
    def with_planning_logic(self,logic): self.s.metadata['planning_logic']=logic;return self
    def with_description(self,desc): self.s.description=desc;return self
class ModuleSpecBuilder(SystemSpecBuilder):
    def __init__(self,name): self.s=Specification(name=name,spec_type=SpecType.MODULE)
class ServiceSpecBuilder(SystemSpecBuilder):
    def __init__(self,name): self.s=Specification(name=name,spec_type=SpecType.SERVICE)
class ToolSpecBuilder(SystemSpecBuilder):
    def __init__(self,name): self.s=Specification(name=name,spec_type=SpecType.CLI_TOOL)
class SpecBuilder:
    function=staticmethod(lambda name:FunctionSpecBuilder(name))
    class_=staticmethod(lambda name:ClassSpecBuilder(name))
    module=staticmethod(lambda name:ModuleSpecBuilder(name))
    pipeline=staticmethod(lambda name:PipelineSpecBuilder(name))
    service=staticmethod(lambda name:ServiceSpecBuilder(name))
    tool=staticmethod(lambda name:ToolSpecBuilder(name))
    capability=staticmethod(lambda name:CapabilitySpecBuilder(name))
    strategy=staticmethod(lambda name:StrategySpecBuilder(name))
    system=staticmethod(lambda name:SystemSpecBuilder(name))
