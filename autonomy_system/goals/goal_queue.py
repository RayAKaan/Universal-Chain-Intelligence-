from __future__ import annotations
import threading, heapq
class PriorityGoalQueue:
    def __init__(self): self.h=[]; self.l=threading.RLock(); self.c=0
    def enqueue(self,goal_record):
        with self.l: self.c+=1; heapq.heappush(self.h,(-goal_record.priority,self.c,goal_record))
    def dequeue(self):
        with self.l: return heapq.heappop(self.h)[2] if self.h else None
    def peek(self):
        with self.l: return self.h[0][2] if self.h else None
    def size(self):
        with self.l: return len(self.h)
    def is_empty(self): return self.size()==0
    def get_all(self):
        with self.l: return [x[2] for x in sorted(self.h)]
    def remove(self,record_id):
        with self.l:
            n=[x for x in self.h if x[2].record_id!=record_id]
            if len(n)==len(self.h): return False
            self.h=n; heapq.heapify(self.h); return True
    def reprioritize(self):
        with self.l: heapq.heapify(self.h)
    def clear(self):
        with self.l: self.h.clear()
