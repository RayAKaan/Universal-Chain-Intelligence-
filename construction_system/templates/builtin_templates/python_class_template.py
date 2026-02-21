from construction_system.models.template import Template

def get_template():
    return Template(template_id='python_class',name='python_class',description='python_class template',template_type='CLASS',language='python',template_string='class {{class_name}}({{base_classes}}):\n    """{{docstring}}"""\n    def __init__(self{{init_params}}):\n{{init_body|indent:8}}\n\n{{methods|indent:4}}\n',variables=[])
