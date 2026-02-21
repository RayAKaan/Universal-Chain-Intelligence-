from __future__ import annotations
import uuid, json
from datetime import datetime, timezone
class ImprovementHistory:
    def __init__(self,db): self.db=db
    def record_event(self,improvement_id,event_type,details): self.db.execute('INSERT INTO improvement_events(event_id,improvement_id,event_type,data,timestamp) VALUES(?,?,?,?,?)',(str(uuid.uuid4()),improvement_id,event_type,json.dumps(details),datetime.now(timezone.utc).isoformat()))
    def get_history(self,improvement_id): return [dict(r) for r in self.db.query('SELECT * FROM improvement_events WHERE improvement_id=? ORDER BY timestamp',(improvement_id,))]
    def get_full_changelog(self): return [dict(r) for r in self.db.query('SELECT * FROM improvement_events ORDER BY timestamp')]
    def search_history(self,query): return [e for e in self.get_full_changelog() if query.lower() in (e.get('data','').lower()+e.get('event_type','').lower())]
