from __future__ import annotations
import threading
from collections import deque
from datetime import datetime, timezone
from autonomy_system.models.system_status import SystemHealth
class SystemState:
    _instance=None; _instance_lock=threading.Lock()
    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None: cls._instance=super().__new__(cls); cls._instance._init()
        return cls._instance
    def _init(self):
        self.lock=threading.RLock(); self.status=SystemHealth.BOOTING; self.autonomy_level='guided'; self.boot_time=datetime.now(timezone.utc)
        self.active_goals={}; self.goal_queue=None; self.phase_states={}; self.errors=deque(maxlen=1000); self.events=deque(maxlen=5000)
        self.counters={'goals_received':0,'goals_completed':0,'goals_failed':0,'capabilities_acquired':0,'improvements_applied':0,'healings_performed':0,'errors_total':0}
    def set_status(self,status):
        with self.lock: self.status=status
    def get_status(self):
        with self.lock: return self.status
    def increment_counter(self,name):
        with self.lock: self.counters[name]=self.counters.get(name,0)+1
    def get_counter(self,name):
        with self.lock: return self.counters.get(name,0)
    def add_error(self,error):
        with self.lock: self.errors.append({'time':datetime.now(timezone.utc).isoformat(),'error':str(error)}); self.increment_counter('errors_total')
    def add_event(self,event):
        with self.lock: self.events.append({'time':datetime.now(timezone.utc).isoformat(),'event':event})
    def get_recent_events(self,limit):
        with self.lock: return list(self.events)[-limit:]
    def get_recent_errors(self,limit):
        with self.lock: return list(self.errors)[-limit:]
    def snapshot(self):
        with self.lock:
            return {'status':self.status.value,'autonomy_level':self.autonomy_level,'boot_time':self.boot_time.isoformat(),'phase_states':self.phase_states,'counters':dict(self.counters),'active_goals':list(self.active_goals.keys()),'errors':list(self.errors),'events':list(self.events)}
    def restore(self,snapshot):
        with self.lock:
            self.autonomy_level=snapshot.get('autonomy_level','guided'); self.phase_states=snapshot.get('phase_states',{}); self.counters.update(snapshot.get('counters',{}))
