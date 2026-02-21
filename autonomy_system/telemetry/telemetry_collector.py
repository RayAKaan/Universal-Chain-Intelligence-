from __future__ import annotations
import threading, time
from datetime import datetime, timezone
from autonomy_system.models.telemetry_point import TelemetryPoint
class TelemetryCollector:
    def __init__(self,core=None): self.core=core; self.running=False; self.thread=None; self.points=[]
    def collect(self):
        p=[TelemetryPoint(category='health',name='overall_score',value=float(getattr(self.core.get_status(),'overall_score',1.0) if self.core else 1.0),source_phase='system',source_component='core'),TelemetryPoint(category='resource',name='cpu_percent',value=20.0,unit='%')]
        self.points.extend(p); return p
    def _loop(self,interval):
        while self.running: self.collect(); time.sleep(interval)
    def start_continuous(self,interval_seconds=30):
        if self.running:return
        self.running=True; self.thread=threading.Thread(target=self._loop,args=(interval_seconds,),daemon=True); self.thread.start()
    def stop_continuous(self): self.running=False
