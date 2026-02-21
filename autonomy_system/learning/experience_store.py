from __future__ import annotations
import sqlite3
from pathlib import Path
from autonomy_system.persistence.serialization import dumps, loads
from autonomy_system.models.learning_record import LearningRecord, LearningType
class ExperienceStore:
    def __init__(self,db_path='data/uci_autonomy.db'):
        Path(db_path).parent.mkdir(parents=True,exist_ok=True); self.conn=sqlite3.connect(db_path,check_same_thread=False); self.conn.row_factory=sqlite3.Row
        self.conn.execute('CREATE TABLE IF NOT EXISTS learning_records(record_id TEXT PRIMARY KEY,learning_type TEXT,confidence REAL,data TEXT,created_at TEXT,applied_count INTEGER,last_applied TEXT)')
    def store(self,record): self.conn.execute('INSERT OR REPLACE INTO learning_records(record_id,learning_type,confidence,data,created_at,applied_count,last_applied) VALUES(?,?,?,?,?,?,?)',(record.record_id,record.learning_type.value,record.confidence,dumps(record),record.created_at.isoformat(),record.applied_count,record.last_applied.isoformat() if record.last_applied else '')); self.conn.commit()
    def query(self,learning_type=None,context=None,limit=100):
        q='SELECT data FROM learning_records'+(' WHERE learning_type=?' if learning_type else '')+' ORDER BY created_at DESC LIMIT ?'
        rows=self.conn.execute(q,((learning_type if isinstance(learning_type,str) else learning_type.value),limit) if learning_type else (limit,)).fetchall()
        out=[]
        for r in rows: d=loads(r['data']); d['learning_type']=LearningType(d['learning_type']); out.append(LearningRecord(**d))
        return out
    def get_applicable(self,context): return self.query(limit=200)
    def get_most_confident(self,limit=10): return sorted(self.query(limit=200),key=lambda x:x.confidence,reverse=True)[:limit]
