from construction_system.models.template import Template

def get_template():
    return Template(template_id='python_function',name='python_function',description='python_function template',template_type='FUNCTION',language='python',template_string='{{decorators}}\ndef {{async_prefix}} {{function_name}}({{parameters}}) -> {{return_type}}:\n    """{{docstring}}"""\n{{body|indent:4}}\n',variables=[])
