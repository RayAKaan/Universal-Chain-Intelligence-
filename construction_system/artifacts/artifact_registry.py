from __future__ import annotations
class ArtifactRegistry:
    def __init__(self):self.by_id={};self.by_type={};self.by_spec={};self.by_component={}
    def add(self,a):
        self.by_id[a.artifact_id]=a;self.by_type.setdefault(a.artifact_type.value,[]).append(a);self.by_spec.setdefault(a.source_spec_id,[]).append(a);self.by_component.setdefault(a.source_component_id,[]).append(a)
    def remove(self,artifact_id):
        if artifact_id in self.by_id: self.by_id.pop(artifact_id)
        self.rebuild_from_store(type('S',(),{'load_all':lambda _ :list(self.by_id.values())})())
    def search(self,filters):
        out=list(self.by_id.values())
        for k,v in filters.items(): out=[a for a in out if getattr(a,k,None)==v]
        return out
    def rebuild_from_store(self,store):
        self.__init__()
        for a in store.load_all(): self.add(a)
