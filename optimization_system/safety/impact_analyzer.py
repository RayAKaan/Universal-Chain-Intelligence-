from __future__ import annotations
from optimization_system.models.bottleneck import ImpactAssessment
class ImpactAnalyzer:
    def analyze_impact(self,modification): return ImpactAssessment(affected_goals=5,affected_capabilities=1,performance_impact_percent=10.0,resource_waste_percent=5.0,description=f'Impact for {modification.target_component}')
    def estimate_blast_radius(self,modification): return {'affected_components':[modification.target_component],'radius':'small'}
