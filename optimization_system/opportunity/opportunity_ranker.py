from __future__ import annotations
class OpportunityRanker:
    def __init__(self,config): self.config=config
    def calculate_priority_score(self,o):
        effort={'trivial':1.0,'low':0.8,'medium':0.5,'high':0.3,'very_high':0.1}.get(o.estimated_effort,0.5)
        est=o.estimated_improvement.get('improvement_percent',0)/100.0; conf=o.estimated_improvement.get('confidence',0.5); urg=o.metadata.get('urgency',0.5)
        w=self.config.OPPORTUNITY_WEIGHTS
        return est*w['estimated_improvement']+conf*w['confidence']+effort*w['effort_inverse']+urg*w['urgency']
    def rank(self,opportunities):
        for o in opportunities:o.priority_score=self.calculate_priority_score(o)
        return sorted(opportunities,key=lambda x:x.priority_score,reverse=True)
    def calculate_roi(self,o): return o.estimated_improvement.get('improvement_percent',0)/{'trivial':1,'low':2,'medium':3,'high':5,'very_high':8}.get(o.estimated_effort,3)
    def filter_actionable(self,ops): return [o for o in ops if not o.prerequisites]
