from __future__ import annotations
class KnowledgeQuery:
    def __init__(self,store): self.store=store
    def query_triples(self,pattern):
        out=[]
        for e in self.store.values():
            if pattern.get('subject') and e.subject!=pattern['subject']: continue
            if pattern.get('predicate') and e.predicate!=pattern['predicate']: continue
            if pattern.get('object') and e.object!=pattern['object']: continue
            out.append(e)
        return out
    def query_by_type(self,knowledge_type): return [e for e in self.store.values() if e.knowledge_type==knowledge_type]
    def query_by_confidence(self,min_confidence): return [e for e in self.store.values() if e.confidence>=min_confidence]
    def query_recent(self,hours=24): return list(self.store.values())
