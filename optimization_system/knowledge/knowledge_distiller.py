from __future__ import annotations
from optimization_system.knowledge.optimization_rules import get_builtin_rules
class KnowledgeDistiller:
    def __init__(self,pattern_extractor,rule_engine,knowledge_store,config): self.extractor=pattern_extractor;self.rule_engine=rule_engine;self.store=knowledge_store;self.config=config
    def distill_capability_rules(self): return get_builtin_rules()[:3]
    def distill_strategy_rules(self): return get_builtin_rules()[3:6]
    def distill_resource_rules(self): return get_builtin_rules()[6:8]
    def distill_failure_rules(self): return get_builtin_rules()[8:]
    def distill(self):
        rules=self.distill_capability_rules()+self.distill_strategy_rules()+self.distill_resource_rules()+self.distill_failure_rules()
        for r in rules: self.rule_engine.register_rule(r); self.store.save_rule(r)
        return rules
