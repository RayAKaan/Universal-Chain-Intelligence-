from __future__ import annotations
import tempfile
from construction_system.sandbox.sandbox_environment import SandboxEnvironment, ResourceLimits
from construction_system.sandbox.output_capture import capture_python_execution
from construction_system.models.sandbox_result import SandboxResult
class SandboxError(Exception):pass
class SandboxManager:
    def __init__(self,config=None):self.config=config;self.active={}
    def create_sandbox(self,name=None):
        d=tempfile.mkdtemp(prefix=(name or 'sandbox_'))
        s=SandboxEnvironment(base_directory=d,resource_limits=ResourceLimits())
        self.active[s.sandbox_id]=s
        return s
    def destroy_sandbox(self,sandbox_id):
        import shutil
        s=self.active.pop(sandbox_id,None)
        if s: shutil.rmtree(s.base_directory,ignore_errors=True)
    def execute_in_sandbox(self,code,sandbox=None):
        s=sandbox or self.create_sandbox()
        r=capture_python_execution(code,s.base_directory,timeout=getattr(self.config,'SANDBOX_TIMEOUT_SECONDS',60) if self.config else 60)
        return SandboxResult(sandbox_id=s.sandbox_id,code_executed=code,execution_success=r['exit_code']==0,stdout=r['stdout'],stderr=r['stderr'],exit_code=r['exit_code'],duration_ms=r['duration_ms'],resource_usage={'cpu_time_ms':r['duration_ms'],'peak_memory_mb':0,'files_created':s.list_files(),'network_calls':0},security_violations=[])
    def execute_file_in_sandbox(self,file_path,sandbox=None):
        code=open(file_path).read();return self.execute_in_sandbox(code,sandbox)
    def list_active_sandboxes(self):return list(self.active.keys())
    def cleanup_all(self):
        for sid in list(self.active): self.destroy_sandbox(sid)
