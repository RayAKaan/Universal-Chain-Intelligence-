from __future__ import annotations
class ComponentVersioner:
    def __init__(self): self.versions={}
    def create_version(self,component_id,version,profile): self.versions.setdefault(component_id,[]).append({'version':version,'profile':profile})
    def get_versions(self,component_id): return self.versions.get(component_id,[])
    def get_best_version(self,component_id,metric):
        vs=self.get_versions(component_id)
        return sorted(vs,key=lambda x:x['profile'].quality_metrics.get('overall_score',0),reverse=True)[0] if vs else {}
    def rollback_to_version(self,component_id,version): return any(v['version']==version for v in self.get_versions(component_id))
    def compare_versions(self,component_id,version_a,version_b): return {'component_id':component_id,'version_a':version_a,'version_b':version_b}
