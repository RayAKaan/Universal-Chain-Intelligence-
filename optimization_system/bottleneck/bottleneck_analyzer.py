from __future__ import annotations
from optimization_system.models.bottleneck import ImpactAssessment, SuggestedAction, BottleneckType
class BottleneckAnalyzer:
    def analyze_impact(self,b): return ImpactAssessment(affected_goals=10,affected_capabilities=3,performance_impact_percent=min(90.0,b.deviation_percent),resource_waste_percent=20.0,description=f'Impact from {b.component}')
    def suggest_actions(self,b):
        if b.bottleneck_type==BottleneckType.SLOW_CAPABILITY:return [SuggestedAction('replace','Replace slow capability',40.0,'medium',1)]
        return [SuggestedAction('investigate','Investigate bottleneck',20.0,'low',2)]
    def correlate_bottlenecks(self,bottlenecks): return [bottlenecks] if bottlenecks else []
    def root_cause_analysis(self,b): return {'root_cause':'high_latency','component':b.component}
