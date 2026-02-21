from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from construction_system.utils.hash_utils import generate_id
from construction_system.utils.file_utils import write_file, read_file, list_files
@dataclass
class ResourceLimits:
    max_cpu_seconds:float=30;max_memory_mb:int=512;max_disk_mb:int=100;max_processes:int=5;max_file_size_mb:int=10;network_allowed:bool=False;max_execution_time_seconds:float=60
@dataclass
class SandboxEnvironment:
    sandbox_id:str=field(default_factory=generate_id);base_directory:str='';resource_limits:ResourceLimits=field(default_factory=ResourceLimits);allowed_imports:list[str]|None=None;blocked_imports:list[str]=field(default_factory=list);environment_variables:dict=field(default_factory=dict);created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
    def write_file(self,relative_path,content):p=Path(self.base_directory)/relative_path;write_file(str(p),content);return str(p)
    def read_file(self,relative_path):return read_file(str(Path(self.base_directory)/relative_path))
    def list_files(self):return list_files(self.base_directory)
    def get_directory(self):return self.base_directory
