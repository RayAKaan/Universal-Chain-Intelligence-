from construction_system.models.template import Template

def get_template():
    return Template(template_id='api_endpoint',name='api_endpoint',description='api_endpoint template',template_type='API',language='python',template_string='def {{endpoint_name}}(request):\n    """{{method}} {{path}}"""\n    return {\'status\':\'ok\',\'data\':request}\n',variables=[])
