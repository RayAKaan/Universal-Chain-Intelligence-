from __future__ import annotations
from optimization_system.models.opportunity import Opportunity, OpportunityType
from optimization_system.opportunity.opportunity_ranker import OpportunityRanker
class OpportunityDetector:
    def __init__(self,bottleneck_detector,performance_analyzer,knowledge_distiller,capability_registry,config): self.bd=bottleneck_detector;self.pa=performance_analyzer;self.kd=knowledge_distiller;self.registry=capability_registry;self.config=config;self.ranker=OpportunityRanker(config)
    def detect_from_bottlenecks(self,bottlenecks):
        out=[]
        for b in bottlenecks:
            t=OpportunityType.REPLACE_SLOW_CAPABILITY if 'SLOW' in b.bottleneck_type.value else OpportunityType.REDUCE_ERROR_RATE
            out.append(Opportunity(t,f'Address {b.bottleneck_type.value}',b.description,b.phase,b.component,{'metric':b.metric_name,'value':b.current_value,'unit':''},{'metric':b.metric_name,'target_value':b.threshold_value,'improvement_percent':max(5.0,min(80.0,b.deviation_percent)),'confidence':0.75},'optimize_component',source='bottleneck_analysis',source_bottleneck_id=b.bottleneck_id,metadata={'urgency':0.8}))
        return out
    def detect_capability_opportunities(self):
        out=[]
        for c in self.registry.get_all():
            lat=(c.metadata or {}).get('latency_ms',100)
            if lat>300: out.append(Opportunity(OpportunityType.REPLACE_SLOW_CAPABILITY,'Replace slow capability',f'{c.name} is slow','phase1',c.capability_id,{'metric':'latency','value':lat,'unit':'ms'},{'metric':'latency','target_value':lat*0.4,'improvement_percent':60.0,'confidence':0.8},'replace',source='manual',metadata={'urgency':0.9}))
        return out
    def detect_strategy_opportunities(self): return []
    def detect_resource_opportunities(self): return []
    def detect_architecture_opportunities(self): return []
    def detect_from_rules(self,rules):
        return [Opportunity(OpportunityType.CUSTOM,f'Rule: {r.name}',r.description,'system','rule_engine',{'metric':r.condition.metric,'value':0,'unit':''},{'metric':r.condition.metric,'target_value':r.condition.threshold,'improvement_percent':20.0,'confidence':r.confidence},'rule_action',source='knowledge_rule',source_rule_id=r.rule_id,metadata={'urgency':0.6}) for r in rules]
    def detect_all(self):
        ops=self.detect_from_bottlenecks(self.bd.detect_all())+self.detect_capability_opportunities()+self.detect_from_rules(self.kd.rule_engine.get_active_rules() if self.kd else [])
        return self.ranker.rank(ops)[:self.config.MAX_OPPORTUNITIES_PER_CYCLE]
