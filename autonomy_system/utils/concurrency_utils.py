from __future__ import annotations
import threading
class SafeCounter:
    def __init__(self): self.v=0; self.l=threading.Lock()
    def inc(self,n=1):
        with self.l: self.v+=n; return self.v
    def get(self):
        with self.l: return self.v
