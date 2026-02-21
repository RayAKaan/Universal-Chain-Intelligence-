from __future__ import annotations
from optimization_system.models.campaign import CampaignStatus
from optimization_system.planner.campaign_executor import CampaignExecutor
class ImprovementCampaignManager:
    def __init__(self): self.executor=CampaignExecutor(); self.states={}
    def execute_phase(self,campaign,phase):
        mapping={'baseline':self.executor.execute_baseline_measurement,'implement':self.executor.execute_improvement_implementation,'experiment':self.executor.execute_experiment,'analysis':self.executor.execute_analysis,'apply_or_rollback':self.executor.execute_apply_or_rollback,'verify':self.executor.execute_verification}
        fn=mapping.get(phase.phase_name)
        return fn(campaign) if fn else {'status':'skipped'}
    def execute_campaign(self,campaign):
        campaign.status=CampaignStatus.running;out={}
        for p in campaign.phases: out[p.phase_name]=self.execute_phase(campaign,p)
        campaign.status=CampaignStatus.completed;self.states[campaign.campaign_id]=campaign.status.value
        return {'campaign_id':campaign.campaign_id,'results':out}
    def pause_campaign(self,campaign_id): self.states[campaign_id]='paused';return True
    def resume_campaign(self,campaign_id): self.states[campaign_id]='running';return True
    def cancel_campaign(self,campaign_id): self.states[campaign_id]='cancelled';return True
    def get_campaign_status(self,campaign_id): return {'campaign_id':campaign_id,'status':self.states.get(campaign_id,'unknown')}
