from __future__ import annotations
from datetime import datetime, timezone
from autonomy_system.models.knowledge_entry import KnowledgeEntry, KnowledgeType
class KnowledgeBase:
    def __init__(self,knowledge_graph,knowledge_indexer,knowledge_query,config): self.graph=knowledge_graph; self.indexer=knowledge_indexer; self.query_engine=knowledge_query; self.config=config; self.entries={}
    def store(self,entry): self.entries[entry.entry_id]=entry; self.graph.add_triple(entry.subject,entry.predicate,entry.object); self.indexer.index(entry); return entry.entry_id
    def query(self,subject=None,predicate=None,object=None): return self.query_engine.query_triples({'subject':subject,'predicate':predicate,'object':object})
    def search(self,text): return [self.entries[eid] for eid in self.indexer.search(text) if eid in self.entries]
    def get_facts_about(self,subject): return [e for e in self.entries.values() if e.subject==subject]
    def learn_fact(self,subject,predicate,object,confidence=1.0,source='system'):
        e=KnowledgeEntry(knowledge_type=KnowledgeType.FACT,subject=subject,predicate=predicate,object=object,confidence=confidence,source=source); return self.store(e)
    def forget(self,entry_id):
        e=self.entries.pop(entry_id,None)
        if e: self.graph.remove_triple(e.subject,e.predicate,e.object); self.indexer.remove(entry_id)
    def get_stats(self): return {'total':len(self.entries),'subjects':len(self.graph.get_all_subjects())}
    def export(self): return [e.__dict__ for e in self.entries.values()]
    def import_knowledge(self,entries):
        c=0
        for d in entries:
            if 'knowledge_type' in d and isinstance(d['knowledge_type'],str): d['knowledge_type']=KnowledgeType(d['knowledge_type'])
            self.store(KnowledgeEntry(**d)); c+=1
        return c
