from construction_system.models.template import Template

def get_template():
    return Template(template_id='data_processor',name='data_processor',description='data_processor template',template_type='DATA_PROCESSOR',language='python',template_string='class {{processor_name}}:\n    def validate_input(self, data):\n        return data is not None\n    def process(self, data):\n{{processing_steps|indent:8}}\n',variables=[])
