from __future__ import annotations
import threading
class ResourceLimiter:
    def apply_limits(self,limits):return None
    def check_limits(self,limits):return {'cpu':0,'memory_mb':0}
    def enforce_timeout(self,func,timeout_seconds):
        out={'v':None,'e':None}
        def run():
            try:out['v']=func()
            except Exception as e:out['e']=e
        t=threading.Thread(target=run);t.start();t.join(timeout_seconds)
        if t.is_alive(): raise TimeoutError('timeout exceeded')
        if out['e']: raise out['e']
        return out['v']
