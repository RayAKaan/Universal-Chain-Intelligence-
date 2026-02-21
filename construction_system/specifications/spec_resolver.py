from __future__ import annotations
class SpecResolver:
    def resolve_dependencies(self,spec,capability_registry):
        available={c.name for c in capability_registry.get_all()} if capability_registry else set()
        missing=[]
        for d in spec.dependencies:
            if d.type=='capability' and d.name not in available and not d.optional: missing.append(d.name)
        spec.metadata['missing_dependencies']=missing
        return spec
    def resolve_templates(self,spec,template_library):
        mapping={'FUNCTION':'python_function','CLASS':'python_class','PIPELINE':'pipeline','API':'api_endpoint','DATA_PROCESSOR':'data_processor','CLI_TOOL':'cli_tool','CAPABILITY_PLUGIN':'capability_plugin','STRATEGY_PLUGIN':'strategy_plugin','DOCKERFILE':'dockerfile','SCRIPT':'shell_script'}
        spec.metadata['template_id']=mapping.get(spec.spec_type.value,'python_function')
        return spec
