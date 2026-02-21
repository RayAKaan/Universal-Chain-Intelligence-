from __future__ import annotations
from datetime import datetime, timezone
class CampaignScheduler:
    def __init__(self): self.scheduled=[]; self.running=[]
    def schedule_campaign(self,campaign,start_time=None): self.scheduled.append((start_time or datetime.now(timezone.utc),campaign))
    def get_scheduled_campaigns(self): return [c for _,c in self.scheduled]
    def get_running_campaigns(self): return list(self.running)
    def cancel_scheduled(self,campaign_id):
        before=len(self.scheduled);self.scheduled=[x for x in self.scheduled if x[1].campaign_id!=campaign_id];return len(self.scheduled)<before
