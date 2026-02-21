from construction_system.models.template import Template

def get_template():
    return Template(template_id='test',name='test',description='test template',template_type='TEST',language='python',template_string='import unittest\nclass {{test_class_name}}(unittest.TestCase):\n{{test_methods|indent:4}}\n',variables=[])
