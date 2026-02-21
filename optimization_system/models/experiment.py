from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
class ExperimentType(str,Enum): CAPABILITY_COMPARISON='CAPABILITY_COMPARISON'; STRATEGY_COMPARISON='STRATEGY_COMPARISON'; CONFIGURATION_COMPARISON='CONFIGURATION_COMPARISON'; TEMPLATE_COMPARISON='TEMPLATE_COMPARISON'; EXECUTION_PATH_COMPARISON='EXECUTION_PATH_COMPARISON'; RESOURCE_ALLOCATION_COMPARISON='RESOURCE_ALLOCATION_COMPARISON'; CUSTOM='CUSTOM'
class ExperimentStatus(str,Enum): DESIGNED='DESIGNED'; RUNNING='RUNNING'; COLLECTING='COLLECTING'; ANALYZING='ANALYZING'; COMPLETED='COMPLETED'; CANCELLED='CANCELLED'
@dataclass
class ExperimentVariant: variant_name:str; description:str=''; configuration:dict=field(default_factory=dict); capability_id:str=''; strategy_name:str=''
@dataclass
class SuccessCriterion: metric:str; operator:str; threshold:float; required:bool=True
@dataclass
class StatisticalResults: control_mean:dict=field(default_factory=dict); treatment_mean:dict=field(default_factory=dict); difference_percent:dict=field(default_factory=dict); p_value:dict=field(default_factory=dict); confidence_interval:dict=field(default_factory=dict); is_significant:dict=field(default_factory=dict); effect_size:dict=field(default_factory=dict)
@dataclass
class Experiment:
    name:str; description:str; experiment_type:ExperimentType; hypothesis:str; control:ExperimentVariant; treatment:ExperimentVariant; metrics_to_compare:list
    experiment_id:str=field(default_factory=lambda:str(uuid4()))
    success_criteria:list=field(default_factory=list); sample_size:int=50; current_samples:int=0
    control_results:list=field(default_factory=list); treatment_results:list=field(default_factory=list)
    statistical_results:StatisticalResults=field(default_factory=StatisticalResults)
    conclusion:str='inconclusive'; status:ExperimentStatus=ExperimentStatus.DESIGNED
    started_at:datetime|None=None; completed_at:datetime|None=None; metadata:dict=field(default_factory=dict)
