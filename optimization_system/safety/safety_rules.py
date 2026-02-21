from __future__ import annotations
RULES=[{'name':'NO_SELF_MODIFICATION'},{'name':'MINIMUM_CAPABILITIES'},{'name':'MINIMUM_STRATEGIES'},{'name':'RESOURCE_SAFETY_MARGIN'},{'name':'ROLLBACK_REQUIRED'},{'name':'EXPERIMENT_REQUIRED'},{'name':'MAX_CONCURRENT_MODIFICATIONS'},{'name':'COOLDOWN_PERIOD'},{'name':'REGRESSION_AUTO_ROLLBACK'},{'name':'MAX_DAILY_MODIFICATIONS'}]
def get_all_rules(): return RULES
def check_rule(rule_name,modification):
    if rule_name=='NO_SELF_MODIFICATION' and modification.target_component in {'safety_governor','improvement_tracker'}: return False,'protected component'
    if rule_name=='ROLLBACK_REQUIRED' and not modification.rollback_available: return False,'rollback required'
    return True,'ok'
