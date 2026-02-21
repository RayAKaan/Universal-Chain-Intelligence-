from __future__ import annotations
import threading, time
from autonomy_system.models.goal_record import GoalRecord, GoalSource, GoalRecordStatus
class GoalManager:
    def __init__(self,intelligence_core,goal_queue,goal_prioritizer,goal_arbitrator,config):
        self.core=intelligence_core; self.queue=goal_queue; self.prioritizer=goal_prioritizer; self.arbitrator=goal_arbitrator; self.config=config; self.history=[]; self.active={}; self.running=False; self.thread=None
    def submit(self,raw_input,source,priority=50,metadata=None):
        r=GoalRecord(source=source,raw_input=raw_input,priority=priority,metadata=metadata or {}); r.priority=self.prioritizer.prioritize(r); r.status=GoalRecordStatus.QUEUED; self.queue.enqueue(r); self.history.append(r); return r
    def cancel(self,record_id):
        if record_id in self.active: self.active[record_id].status=GoalRecordStatus.CANCELLED; return True
        return self.queue.remove(record_id)
    def pause(self,record_id):
        if record_id in self.active: self.active[record_id].status=GoalRecordStatus.PAUSED; return True
        return False
    def resume(self,record_id):
        if record_id in self.active and self.active[record_id].status==GoalRecordStatus.PAUSED: self.active[record_id].status=GoalRecordStatus.EXECUTING; return True
        return False
    def get_status(self,record_id):
        for r in self.history:
            if r.record_id==record_id:return r
        return None
    def get_active_goals(self): return list(self.active.values())
    def get_queue_status(self): return {'queued':self.queue.size(),'active':len(self.active)}
    def get_history(self,limit=100): return self.history[-limit:]
    def process_next(self):
        g=self.queue.dequeue();
        if not g:return None
        self.active[g.record_id]=g
        g.status=GoalRecordStatus.INTERPRETING; t=time.time(); result=self.core.process_goal(g); result.execution_time_ms=(time.time()-t)*1000
        self.active.pop(g.record_id,None)
        return result
    def _loop(self):
        while self.running:
            self.process_next(); time.sleep(self.config.GOAL_PROCESSING_INTERVAL_MS/1000)
    def start_processing(self):
        if self.running:return
        self.running=True; self.thread=threading.Thread(target=self._loop,daemon=True); self.thread.start()
    def stop_processing(self): self.running=False
