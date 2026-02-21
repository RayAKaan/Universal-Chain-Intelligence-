from __future__ import annotations
from datetime import datetime, timezone
class RuleEngine:
    def __init__(self): self.rules=[]
    def register_rule(self,rule): self.rules.append(rule)
    def deactivate_rule(self,rule_id):
        for r in self.rules:
            if r.rule_id==rule_id:r.enabled=False
    def get_active_rules(self): return [r for r in self.rules if r.enabled]
    def evaluate_rules(self,current_metrics):
        out=[]
        for r in self.get_active_rules():
            v=current_metrics.get(r.condition.metric)
            if v is None: continue
            ok={'gt':v>r.condition.threshold,'lt':v<r.condition.threshold,'gte':v>=r.condition.threshold,'lte':v<=r.condition.threshold}.get(r.condition.operator,False)
            if ok: r.trigger_count+=1; r.last_triggered=datetime.now(timezone.utc); out.append((r,{'value':v}))
        return out
    def execute_rule_action(self,rule,context): return {'action':rule.action.action_type,'context':context}
