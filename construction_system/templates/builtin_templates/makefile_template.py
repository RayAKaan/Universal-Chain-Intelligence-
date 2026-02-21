from construction_system.models.template import Template

def get_template():
    return Template(template_id='makefile',name='makefile',description='makefile template',template_type='MAKEFILE',language='python',template_string='install:\n\tpip install -r requirements.txt\n\ntest:\n\tpython -m unittest discover\n\nrun:\n\tpython {{entrypoint}}\n',variables=[])
