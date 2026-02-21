from __future__ import annotations
from datetime import datetime, timezone
from autonomy_system.models.acquisition_record import AcquisitionRecord, AcquisitionType, AcquisitionStatus
class AcquisitionEngine:
    def __init__(self,source_registry,package_installer,capability_fetcher,dependency_resolver,acquisition_safety,phase1_bridge,phase3_bridge,autonomy_controller,config):
        self.sources=source_registry; self.installer=package_installer; self.fetcher=capability_fetcher; self.deps=dependency_resolver; self.safety=acquisition_safety; self.phase1=phase1_bridge; self.phase3=phase3_bridge; self.autonomy=autonomy_controller; self.config=config; self.history=[]
    def search(self,query):
        out=[]
        for s in self.sources.get_sources():
            if not s.get('enabled'): continue
            out += self.fetcher.search_pypi(query) if s['type']=='pypi' else self.fetcher.search_local(query)
        return out
    def acquire(self,name,reason,requested_by='system'):
        rec=AcquisitionRecord(acquisition_type=AcquisitionType.PYTHON_PACKAGE,name=name,reason=reason,requested_by=requested_by,status=AcquisitionStatus.REQUESTED)
        if not self.autonomy.can_perform('acquire_capability'):
            rec.status=AcquisitionStatus.REJECTED; rec.metadata={'reason':'autonomy restrictions'}; self.history.append(rec); return rec
        safe,issues=self.safety.check_safe(name,'pypi'); rec.safety_check_passed=safe; rec.safety_report={'issues':issues}
        if not safe: rec.status=AcquisitionStatus.REJECTED; self.history.append(rec); return rec
        rec.status=AcquisitionStatus.INSTALLING
        ok=self.installer.install_python_package(name)
        rec.status=AcquisitionStatus.REGISTERED if ok else AcquisitionStatus.FAILED
        rec.completed_at=datetime.now(timezone.utc); self.history.append(rec); return rec
    def acquire_for_goal(self,goal,missing_capability_type): return self.acquire(missing_capability_type,f'missing for goal {goal.record_id}','goal_resolver')
    def get_recommendations(self): return [{'name':'pandas','reason':'common data processing gap'}]
    def get_acquisition_history(self): return self.history
    def get_pending_acquisitions(self): return [h for h in self.history if h.status in {AcquisitionStatus.REQUESTED,AcquisitionStatus.INSTALLING}]
