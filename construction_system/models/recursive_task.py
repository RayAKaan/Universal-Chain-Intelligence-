from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from construction_system.utils.hash_utils import generate_id
from construction_system.models.specification import Specification
class RecursiveTaskType(str,Enum):BUILD_SYSTEM='BUILD_SYSTEM';BUILD_COMPONENT='BUILD_COMPONENT';BUILD_PIPELINE='BUILD_PIPELINE';BUILD_CAPABILITY='BUILD_CAPABILITY';BUILD_STRATEGY='BUILD_STRATEGY';BUILD_TOOL='BUILD_TOOL';BUILD_SERVICE='BUILD_SERVICE';GENERATE_CODE='GENERATE_CODE';GENERATE_TESTS='GENERATE_TESTS';GENERATE_CONFIG='GENERATE_CONFIG';COMPOSE_SYSTEM='COMPOSE_SYSTEM';INTEGRATE_COMPONENT='INTEGRATE_COMPONENT'
@dataclass
class ResourceBudget:
    max_cpu_seconds:float=300;max_memory_mb:int=2048;max_disk_mb:int=500;max_files:int=200;max_lines_of_code:int=50000;max_child_tasks:int=20;budget_used:dict=field(default_factory=dict)
@dataclass
class RecursiveTask:
    task_id:str=field(default_factory=generate_id);parent_task_id:str|None=None;root_task_id:str='';name:str='';description:str='';task_type:RecursiveTaskType=RecursiveTaskType.BUILD_SYSTEM;specification:Specification|None=None;depth:int=0;max_depth:int=10;resource_budget:ResourceBudget=field(default_factory=ResourceBudget);child_task_ids:list[str]=field(default_factory=list);status:str='pending';result:object=None;error:str='';created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc));started_at:datetime|None=None;completed_at:datetime|None=None
