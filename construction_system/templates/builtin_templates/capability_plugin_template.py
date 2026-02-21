from construction_system.models.template import Template

def get_template():
    return Template(template_id='capability_plugin',name='capability_plugin',description='capability_plugin template',template_type='CAPABILITY_PLUGIN',language='python',template_string="class {{plugin_name}}:\n    def execute(self, payload):\n{{processing_logic|indent:8}}\n    def validate(self, payload):\n        return isinstance(payload, dict)\n    def get_requirements(self):\n        return {'threads':1}\n",variables=[])
