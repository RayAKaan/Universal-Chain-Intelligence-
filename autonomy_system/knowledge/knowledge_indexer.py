from __future__ import annotations
class KnowledgeIndexer:
    def __init__(self): self.idx={}
    def index(self,entry):
        txt=f"{entry.subject} {entry.predicate} {entry.object}".lower()
        for t in txt.split(): self.idx.setdefault(t,set()).add(entry.entry_id)
    def search(self,query):
        terms=query.lower().split();
        sets=[self.idx.get(t,set()) for t in terms]
        if not sets:return []
        return list(set.intersection(*sets)) if sets else []
    def remove(self,entry_id):
        for k in list(self.idx):
            self.idx[k].discard(entry_id)
            if not self.idx[k]: self.idx.pop(k,None)
    def rebuild(self): self.idx={}
