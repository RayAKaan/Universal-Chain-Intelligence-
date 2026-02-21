from __future__ import annotations
from construction_system.models.provenance_record import ProvenanceRecord
class ProvenanceError(Exception):pass
class ProvenanceTracker:
    def __init__(self,store):self.store=store
    def _save(self,r):self.store.save(r);return r
    def record_creation(self,artifact,source_spec,source_blueprint,source_task,template_used=None,parent_artifacts=None):
        return self._save(ProvenanceRecord(artifact_id=artifact.artifact_id,action='created',actor='construction_system',source_spec_id=source_spec.spec_id,source_blueprint_id=source_blueprint.blueprint_id,source_task_id=source_task.task_id,template_used=template_used or '',parent_artifacts=parent_artifacts or []))
    def record_modification(self,artifact_id,action,details):return self._save(ProvenanceRecord(artifact_id=artifact_id,action=action,metadata=details))
    def record_testing(self,artifact_id,test_results):return self._save(ProvenanceRecord(artifact_id=artifact_id,action='tested',verification={'tests_passed':test_results.get('passed',0)>0}))
    def record_deployment(self,artifact_id,deployment_details):return self._save(ProvenanceRecord(artifact_id=artifact_id,action='deployed',metadata=deployment_details))
    def record_registration(self,artifact_id,registration_type,registration_id):return self._save(ProvenanceRecord(artifact_id=artifact_id,action='registered',metadata={'type':registration_type,'id':registration_id}))
    def get_provenance(self,artifact_id):return self.store.load_by_artifact(artifact_id)
    def get_lineage(self,artifact_id):
        recs=self.get_provenance(artifact_id);return {'artifact_id':artifact_id,'records':[r.record_id for r in recs],'parents':[p for r in recs for p in r.parent_artifacts]}
    def get_descendants(self,artifact_id):
        out=[]
        for r in self.store.load_all():
            if artifact_id in r.parent_artifacts: out.append(r.artifact_id)
        return out
    def get_full_lineage_graph(self,root_artifact_id):
        from construction_system.provenance.lineage_graph import LineageGraph
        g=LineageGraph()
        for r in self.store.load_all(): g.add_record(r)
        return g.to_dict()
