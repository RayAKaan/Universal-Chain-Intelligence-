from __future__ import annotations
import threading
class TemplateRegistry:
    def __init__(self):self._lock=threading.RLock();self._t={}
    def register(self,template):
        with self._lock:self._t[template.template_id]=template
    def get(self,template_id):return self._t[template_id]
    def search(self,filters):
        out=list(self._t.values())
        for k,v in filters.items(): out=[t for t in out if getattr(t,k,None)==v]
        return out
    def get_all(self):return list(self._t.values())
