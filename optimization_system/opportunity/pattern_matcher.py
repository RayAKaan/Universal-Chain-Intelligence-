from __future__ import annotations
from optimization_system.models.opportunity import Opportunity, OpportunityType
class PatternMatcher:
    def __init__(self): self.patterns={}
    def register_pattern(self,name,detector_func): self.patterns[name]=detector_func
    def list_patterns(self): return list(self.patterns)
    def match_known_patterns(self,metrics,profiles):
        out=[]
        for p in profiles:
            if p.performance_metrics.get('avg_latency_ms',0)>500:
                out.append(Opportunity(OpportunityType.REPLACE_SLOW_CAPABILITY,'Overloaded component',f'{p.component_name} high latency',p.phase,p.component_name,{'metric':'latency','value':p.performance_metrics.get('avg_latency_ms',0),'unit':'ms'},{'metric':'latency','target_value':p.performance_metrics.get('avg_latency_ms',0)*0.5,'improvement_percent':50.0,'confidence':0.8},'replace_or_optimize',source='pattern_matching'))
        return out
