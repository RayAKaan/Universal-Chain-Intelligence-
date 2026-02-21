from __future__ import annotations
from datetime import datetime
from optimization_system.persistence.serialization import serialize, deserialize
from optimization_system.models.experiment import Experiment, ExperimentType, ExperimentStatus, ExperimentVariant, StatisticalResults
class ExperimentStore:
    def __init__(self,db): self.db=db
    def save(self,e): self.db.execute('INSERT OR REPLACE INTO experiments(experiment_id,experiment_type,status,conclusion,data,started_at,completed_at) VALUES(?,?,?,?,?,?,?)',(e.experiment_id,e.experiment_type.value,e.status.value,e.conclusion,serialize(e),e.started_at.isoformat() if e.started_at else '',e.completed_at.isoformat() if e.completed_at else ''))
    def _load(self,row):
        d=deserialize(row['data']);d['experiment_type']=ExperimentType(d['experiment_type']);d['status']=ExperimentStatus(d['status']);d['control']=ExperimentVariant(**d['control']);d['treatment']=ExperimentVariant(**d['treatment']);d['statistical_results']=StatisticalResults(**d.get('statistical_results',{}))
        if d.get('started_at'): d['started_at']=datetime.fromisoformat(d['started_at'])
        if d.get('completed_at'): d['completed_at']=datetime.fromisoformat(d['completed_at'])
        return Experiment(**d)
    def load(self,experiment_id):
        r=self.db.query('SELECT * FROM experiments WHERE experiment_id=?',(experiment_id,));return self._load(r[0]) if r else None
    def load_all(self): return [self._load(r) for r in self.db.query('SELECT * FROM experiments ORDER BY started_at DESC')]
    def load_by_status(self,status):
        s=status.value if hasattr(status,'value') else status
        return [self._load(r) for r in self.db.query('SELECT * FROM experiments WHERE status=?',(s,))]
