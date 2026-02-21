from construction_system.models.template import Template

def get_template():
    return Template(template_id='config',name='config',description='config template',template_type='CONFIGURATION',language='python',template_string='CONFIG = {{config_dict}}\n',variables=[])
