from __future__ import annotations
import threading, time
class ImprovementScheduler:
    def __init__(self,cycle_manager,opportunity_detector,optimization_planner,config): self.cm=cycle_manager;self.detector=opportunity_detector;self.planner=optimization_planner;self.config=config;self.running=False;self.thread=None;self.history=[]
    def run_cycle(self):
        r=self.cm.execute_cycle(); self.history.append(r); return r
    def start(self,interval_minutes=60):
        if self.running:return
        self.running=True
        def loop():
            while self.running:
                self.run_cycle(); time.sleep(max(1,interval_minutes*60))
        self.thread=threading.Thread(target=loop,daemon=True); self.thread.start()
    def stop(self): self.running=False
    def schedule_next_cycle(self,delay_minutes=None): return None
    def get_cycle_history(self): return list(self.history)
