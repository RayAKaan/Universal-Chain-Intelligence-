from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from construction_system.utils.hash_utils import generate_id
class BuildStatus(str,Enum):SUCCESS='SUCCESS';PARTIAL_SUCCESS='PARTIAL_SUCCESS';FAILURE='FAILURE';VALIDATION_FAILED='VALIDATION_FAILED';TEST_FAILED='TEST_FAILED';SANDBOX_FAILED='SANDBOX_FAILED';INTEGRATION_FAILED='INTEGRATION_FAILED'
@dataclass
class BuildResult:
    result_id:str=field(default_factory=generate_id);blueprint_id:str='';spec_id:str='';status:BuildStatus=BuildStatus.SUCCESS;components_built:list[str]=field(default_factory=list);artifacts_created:list[str]=field(default_factory=list);files_created:list[str]=field(default_factory=list);code_stats:dict=field(default_factory=lambda:{'total_files':0,'total_lines':0,'total_functions':0,'total_classes':0,'total_tests':0});validation_results:dict=field(default_factory=lambda:{'syntax_valid':True,'imports_valid':True,'tests_passed':0,'tests_failed':0,'static_analysis_issues':[]});sandbox_results:dict=field(default_factory=dict);integration_results:dict=field(default_factory=lambda:{'capability_registered':False,'capability_id':'','strategy_registered':False,'strategy_name':''});build_duration_ms:float=0.0;errors:list[str]=field(default_factory=list);warnings:list[str]=field(default_factory=list);created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc));code_units:list=field(default_factory=list);blueprint:object=None;test_code:str='';artifacts:list=field(default_factory=list)
