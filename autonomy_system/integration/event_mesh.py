from __future__ import annotations
import fnmatch, threading
class EventMesh:
    def __init__(self): self.subs={}; self.events=[]; self.lock=threading.RLock(); self.seq=0
    def subscribe(self,pattern,handler):
        with self.lock: self.seq+=1; sid=f's{self.seq}'; self.subs[sid]=(pattern,handler); return sid
    def unsubscribe(self,sid):
        with self.lock: self.subs.pop(sid,None)
    def publish(self,event_type,data):
        ev={'event_type':event_type,'data':data};
        with self.lock:
            self.events.append(ev); subs=list(self.subs.values())
        for pat,h in subs:
            if fnmatch.fnmatch(event_type,pat):
                try: h(ev)
                except Exception: pass
    def get_event_stream(self,filter=None,limit=100):
        with self.lock:
            es=self.events[-limit:]
        return [e for e in es if (not filter or fnmatch.fnmatch(e['event_type'],filter))]
