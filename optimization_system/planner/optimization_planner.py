from __future__ import annotations
from optimization_system.models.campaign import Campaign, CampaignPhase
class OptimizationPlanner:
    def __init__(self,opportunity_detector,phase2_bridge,phase3_bridge,safety_governor,config): self.detector=opportunity_detector;self.p2=phase2_bridge;self.p3=phase3_bridge;self.safety=safety_governor;self.config=config
    def generate_improvement_plan(self,opportunity): return self.p2.plan_improvement(opportunity.description)
    def plan_improvement(self,opportunity):
        c=Campaign(name=f'Campaign: {opportunity.title}',description=opportunity.description,goal=opportunity.title,target_metric=opportunity.estimated_improvement.get('metric','custom'),target_improvement_percent=opportunity.estimated_improvement.get('improvement_percent',10.0),opportunities=[opportunity.opportunity_id],phases=[CampaignPhase('baseline','Baseline',['measure']),CampaignPhase('implement','Implement',['build']),CampaignPhase('experiment','Experiment',['ab']),CampaignPhase('analysis','Analyze',['compare']),CampaignPhase('apply_or_rollback','Apply or rollback',['apply']),CampaignPhase('verify','Verify',['verify'])])
        c.metadata['phase2_plan']=self.generate_improvement_plan(opportunity)
        return c
    def plan_batch_improvements(self,opportunities,max_concurrent=3): return [self.plan_improvement(o) for o in opportunities[:max_concurrent]]
    def estimate_campaign_duration(self,campaign): return len(campaign.phases)*300.0
    def estimate_campaign_risk(self,campaign): return 'medium'
