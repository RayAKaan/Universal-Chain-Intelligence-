from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4
class CampaignStatus(str,Enum): planned='planned'; running='running'; paused='paused'; completed='completed'; failed='failed'; cancelled='cancelled'
@dataclass
class CampaignPhase: phase_name:str; description:str; actions:list; status:str='pending'; started_at:datetime|None=None; completed_at:datetime|None=None
@dataclass
class Campaign:
    name:str; description:str; goal:str; target_metric:str; target_improvement_percent:float
    campaign_id:str=field(default_factory=lambda:str(uuid4()))
    opportunities:list=field(default_factory=list); improvements:list=field(default_factory=list); experiments:list=field(default_factory=list); modifications:list=field(default_factory=list)
    phases:list=field(default_factory=list); status:CampaignStatus=CampaignStatus.planned
    before_baseline:dict=field(default_factory=dict); after_baseline:dict=field(default_factory=dict); total_improvement:dict=field(default_factory=dict)
    started_at:datetime|None=None; completed_at:datetime|None=None; metadata:dict=field(default_factory=dict)
