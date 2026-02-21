from construction_system.models.template import Template

def get_template():
    return Template(template_id='shell_script',name='shell_script',description='shell_script template',template_type='SCRIPT',language='python',template_string='#!/usr/bin/env bash\nset -e\n{{commands}}\n',variables=[])
