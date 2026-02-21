from construction_system.models.template import Template

def get_template():
    return Template(template_id='pipeline',name='pipeline',description='pipeline template',template_type='PIPELINE',language='python',template_string='class {{pipeline_name}}Pipeline:\n    def __init__(self):\n        self.stages = [{{stages}}]\n    def run(self, data):\n        for s in self.stages:\n            data = s.process(data)\n        return data\n',variables=[])
