from construction_system.models.template import Template

def get_template():
    return Template(template_id='strategy_plugin',name='strategy_plugin',description='strategy_plugin template',template_type='STRATEGY_PLUGIN',language='python',template_string="from planning_system.strategies.base_strategy import BaseStrategy\nclass {{strategy_name}}(BaseStrategy):\n    name='{{strategy_name}}'\n    description='{{description}}'\n    def plan(self, goal, context):\n{{planning_logic|indent:8}}\n    def is_suitable(self, goal, context):\n        return {{suitability}}\n",variables=[])
