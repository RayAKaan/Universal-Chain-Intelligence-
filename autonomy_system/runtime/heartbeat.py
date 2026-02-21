from __future__ import annotations
import threading, time
from datetime import datetime, timezone
class Heartbeat:
    def __init__(self): self.last=None; self.running=False; self.thread=None
    def _loop(self,interval):
        while self.running: self.last=datetime.now(timezone.utc); time.sleep(interval)
    def start(self,interval_seconds=10):
        if self.running:return
        self.running=True; self.thread=threading.Thread(target=self._loop,args=(interval_seconds,),daemon=True); self.thread.start()
    def stop(self): self.running=False
    def get_last_heartbeat(self): return self.last
    def is_alive(self,timeout_seconds=30):
        if not self.last:return False
        return (datetime.now(timezone.utc)-self.last).total_seconds()<timeout_seconds
