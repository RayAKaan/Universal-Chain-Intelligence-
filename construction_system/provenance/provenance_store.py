from __future__ import annotations

from construction_system.persistence.serialization import deserialize_provenance_record, serialize_provenance_record


class ProvenanceStore:
    def __init__(self, db):
        self.db = db

    def save(self, r):
        self.db.execute(
            "INSERT OR REPLACE INTO provenance(record_id,artifact_id,action,actor,data,timestamp) VALUES(?,?,?,?,?,datetime('now'))",
            (r.record_id, r.artifact_id, r.action, r.actor, serialize_provenance_record(r)),
        )

    def load(self, record_id):
        x = self.db.query("SELECT data FROM provenance WHERE record_id=?", (record_id,))
        return deserialize_provenance_record(x[0]["data"]) if x else None

    def load_by_artifact(self, artifact_id):
        return [deserialize_provenance_record(r["data"]) for r in self.db.query("SELECT data FROM provenance WHERE artifact_id=?", (artifact_id,))]

    def load_all(self):
        return [deserialize_provenance_record(r["data"]) for r in self.db.query("SELECT data FROM provenance")]
