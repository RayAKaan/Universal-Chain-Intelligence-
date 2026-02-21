from __future__ import annotations
import time
class ShutdownHandler:
    def __init__(self): self.cleanup=[]
    def register_cleanup(self,name,function,priority): self.cleanup.append({'name':name,'function':function,'priority':priority})
    def execute_shutdown(self,graceful=True,timeout_seconds=30):
        start=time.time()
        for c in sorted(self.cleanup,key=lambda x:x['priority']):
            try: c['function']()
            except Exception: pass
            if time.time()-start>timeout_seconds: break
