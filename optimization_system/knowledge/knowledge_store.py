from __future__ import annotations
import uuid, json
from optimization_system.persistence.serialization import serialize, deserialize
from optimization_system.models.optimization_rule import OptimizationRule, RuleCondition, RuleAction
class KnowledgeStore:
    def __init__(self,db): self.db=db
    def save_rule(self,rule): self.db.execute('INSERT OR REPLACE INTO optimization_rules(rule_id,name,rule_type,enabled,data,created_at) VALUES(?,?,?,?,?,?)',(rule.rule_id,rule.name,rule.rule_type,1 if rule.enabled else 0,serialize(rule),rule.created_at.isoformat()))
    def _to_rule(self,row):
        d=deserialize(row['data']); d['condition']=RuleCondition(**d['condition']); d['action']=RuleAction(**d['action']); return OptimizationRule(**d)
    def load_rule(self,rule_id):
        r=self.db.query('SELECT * FROM optimization_rules WHERE rule_id=?',(rule_id,)); return self._to_rule(r[0]) if r else None
    def load_all_rules(self): return [self._to_rule(r) for r in self.db.query('SELECT * FROM optimization_rules')]
    def load_active_rules(self): return [self._to_rule(r) for r in self.db.query('SELECT * FROM optimization_rules WHERE enabled=1')]
    def update_rule(self,rule): self.save_rule(rule)
    def delete_rule(self,rule_id): self.db.execute('DELETE FROM optimization_rules WHERE rule_id=?',(rule_id,))
    def save_pattern(self,pattern): self.db.execute('INSERT INTO knowledge_patterns(pattern_id,pattern_type,data,created_at) VALUES(?,?,?,datetime("now"))',(str(uuid.uuid4()),pattern.get('type','generic'),json.dumps(pattern)))
    def load_patterns(self,pattern_type=None):
        rows=self.db.query('SELECT data FROM knowledge_patterns'+(' WHERE pattern_type=?' if pattern_type else ''),(pattern_type,) if pattern_type else ())
        return [json.loads(r['data']) for r in rows]
