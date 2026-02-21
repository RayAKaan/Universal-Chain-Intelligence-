from __future__ import annotations
from construction_system.templates.template_engine import TemplateEngine
from construction_system.templates.template_registry import TemplateRegistry
from construction_system.models.template import Template
from construction_system.templates.builtin_templates import python_function_template, python_class_template, pipeline_template, api_endpoint_template, data_processor_template, cli_tool_template, test_template, config_template, dockerfile_template, makefile_template, shell_script_template, capability_plugin_template, strategy_plugin_template
class TemplateLibrary:
    def __init__(self,template_registry=None,config=None):
        self.registry=template_registry or TemplateRegistry();self.engine=TemplateEngine();self.config=config
        self._load_builtin()
    def _load_builtin(self):
        for fn in [python_function_template.get_template,python_class_template.get_template,pipeline_template.get_template,api_endpoint_template.get_template,data_processor_template.get_template,cli_tool_template.get_template,test_template.get_template,config_template.get_template,dockerfile_template.get_template,makefile_template.get_template,shell_script_template.get_template,capability_plugin_template.get_template,strategy_plugin_template.get_template]:
            self.register_template(fn())
    def get_template(self,template_id):return self.registry.get(template_id)
    def get_templates_by_type(self,t):return self.registry.search({'template_type':t})
    def get_templates_by_language(self,lang):return self.registry.search({'language':lang})
    def search_templates(self,q):
        q=q.lower();return [t for t in self.registry.get_all() if q in t.name.lower() or q in t.description.lower()]
    def register_template(self,template):self.registry.register(template);return template.template_id
    def unregister_template(self,template_id):self.registry._t.pop(template_id,None)
    def render_template(self,template_id,variables):
        t=self.get_template(template_id)
        for v in t.variables:
            if v.get('required') and v['name'] not in variables: raise ValueError(f"missing variable {v['name']}")
        return self.engine.render(t.template_string,variables)
    def list_all(self):return self.registry.get_all()
    def get_stats(self):
        all_t=self.list_all();return {'count':len(all_t),'by_language':{k:len([x for x in all_t if x.language==k]) for k in set(t.language for t in all_t)}}
