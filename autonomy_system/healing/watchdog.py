from __future__ import annotations
import threading, time
class Watchdog:
    def __init__(self): self.monitors={}; self.running=False; self.thread=None; self.issues=[]; self.callbacks=[]
    def register_monitor(self,name,check_func,critical=False): self.monitors[name]=(check_func,critical)
    def on_issue_detected(self,callback): self.callbacks.append(callback)
    def _loop(self,interval):
        while self.running:
            for n,(fn,critical) in list(self.monitors.items()):
                try:
                    ok=fn()
                    if ok is False:
                        issue={'monitor':n,'critical':critical}; self.issues.append(issue)
                        for cb in self.callbacks: cb(issue)
                except Exception:
                    issue={'monitor':n,'critical':critical}; self.issues.append(issue)
            time.sleep(interval)
    def start(self,interval_seconds=30):
        if self.running:return
        self.running=True; self.thread=threading.Thread(target=self._loop,args=(interval_seconds,),daemon=True); self.thread.start()
    def stop(self): self.running=False
    def get_status(self): return {'running':self.running,'issues':self.issues[-20:]}
