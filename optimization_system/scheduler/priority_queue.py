from __future__ import annotations
import heapq
class PriorityQueue:
    def __init__(self): self.h=[]; self.c=0
    def add(self,item,priority): self.c+=1; heapq.heappush(self.h,(-priority,self.c,item))
    def pop(self): return heapq.heappop(self.h)[2] if self.h else None
    def peek(self): return self.h[0][2] if self.h else None
    def is_empty(self): return not self.h
    def size(self): return len(self.h)
    def clear(self): self.h.clear()
