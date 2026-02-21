from __future__ import annotations
import json
from optimization_system.models.improvement import ImprovementStatus
class ImprovementTracker:
    def __init__(self,db,history): self.db=db;self.history=history;self.cache={}
    def record_improvement(self,improvement):
        self.cache[improvement.improvement_id]=improvement
        self.db.execute('INSERT OR REPLACE INTO improvements(improvement_id,improvement_type,target_phase,status,data,created_at) VALUES(?,?,?,?,?,?)',(improvement.improvement_id,improvement.improvement_type.value,improvement.target_phase,improvement.status.value,json.dumps(improvement.__dict__,default=str),improvement.created_at.isoformat()))
        self.history.record_event(improvement.improvement_id,'recorded',{'title':improvement.title})
    def update_improvement(self,improvement_id,updates):
        i=self.cache.get(improvement_id)
        if not i:return
        for k,v in updates.items(): setattr(i,k,v)
        self.record_improvement(i)
    def get_improvement(self,improvement_id): return self.cache.get(improvement_id)
    def get_all_improvements(self): return list(self.cache.values())
    def get_improvements_by_status(self,status): s=status.value if hasattr(status,'value') else status; return [i for i in self.cache.values() if i.status.value==s]
    def get_improvements_by_phase(self,phase): return [i for i in self.cache.values() if i.target_phase==phase]
    def get_improvements_by_type(self,improvement_type): t=improvement_type.value if hasattr(improvement_type,'value') else improvement_type; return [i for i in self.cache.values() if i.improvement_type.value==t]
    def get_improvement_timeline(self): return [{'id':i.improvement_id,'title':i.title,'status':i.status.value,'created_at':i.created_at.isoformat()} for i in sorted(self.cache.values(),key=lambda x:x.created_at)]
    def get_improvement_impact(self):
        items=self.get_all_improvements()
        return {'total_improvements':len(items),'successful':len([i for i in items if i.status.value in {'APPLIED','VERIFIED'}]),'rolled_back':len([i for i in items if i.status==ImprovementStatus.ROLLED_BACK]),'net_latency_improvement_percent':sum(i.improvement_percent.get('latency',0) for i in items),'net_reliability_improvement_percent':sum(i.improvement_percent.get('reliability',0) for i in items),'net_resource_savings_percent':sum(i.improvement_percent.get('resource',0) for i in items),'capabilities_added':0,'capabilities_replaced':len([i for i in items if 'CAPABILITY' in i.improvement_type.value]),'capabilities_removed':0,'strategies_added':len([i for i in items if i.improvement_type.value=='STRATEGY_CREATION']),'strategies_replaced':len([i for i in items if 'STRATEGY' in i.improvement_type.value and 'REPLACEMENT' in i.improvement_type.value])}
