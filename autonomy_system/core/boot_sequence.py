from __future__ import annotations
from dataclasses import dataclass
import time
@dataclass
class BootStep: name:str; function:callable; required:bool=True; timeout_seconds:float=30.0; retry_count:int=1
class BootSequence:
    def __init__(self,steps=None): self.steps=steps or []
    def execute(self):
        start=time.time(); results=[]; errors=[]; completed=0; failed=0
        for s in self.steps:
            ok=False; err=''
            for _ in range(max(1,s.retry_count)):
                try: s.function(); ok=True; break
                except Exception as e: err=str(e)
            results.append({'name':s.name,'ok':ok,'error':err});
            if ok: completed+=1
            else:
                failed+=1; errors.append(f'{s.name}: {err}')
                if s.required: break
        return {'success':failed==0,'steps_completed':completed,'steps_failed':failed,'total_duration_ms':(time.time()-start)*1000,'step_results':results,'errors':errors}
