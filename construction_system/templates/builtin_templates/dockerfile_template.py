from construction_system.models.template import Template

def get_template():
    return Template(template_id='dockerfile',name='dockerfile',description='dockerfile template',template_type='DOCKERFILE',language='python',template_string='FROM {{base_image}}\nWORKDIR /app\nCOPY . /app\nRUN pip install -r requirements.txt\nENTRYPOINT ["python", "{{entrypoint}}"]\n',variables=[])
