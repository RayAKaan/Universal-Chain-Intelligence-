from __future__ import annotations

from construction_system.models.artifact import Artifact
from construction_system.persistence.serialization import deserialize_artifact, serialize_artifact


class ArtifactStore:
    def __init__(self, db):
        self.db = db

    def save(self, a: Artifact):
        self.db.execute(
            "INSERT OR REPLACE INTO artifacts(artifact_id,name,artifact_type,file_path,checksum,source_spec_id,source_blueprint_id,data,created_at) VALUES(?,?,?,?,?,?,?,?,datetime('now'))",
            (a.artifact_id, a.name, a.artifact_type.value, a.file_path, a.checksum, a.source_spec_id, a.source_blueprint_id, serialize_artifact(a)),
        )

    def load(self, artifact_id):
        rows = self.db.query("SELECT data FROM artifacts WHERE artifact_id=?", (artifact_id,))
        return deserialize_artifact(rows[0]["data"]) if rows else None

    def load_all(self):
        return [deserialize_artifact(x["data"]) for x in self.db.query("SELECT data FROM artifacts")]

    def search(self, query):
        out = self.load_all()
        for k, v in query.items():
            out = [a for a in out if getattr(a, k, None) == v]
        return out

    def delete(self, artifact_id):
        self.db.execute("DELETE FROM artifacts WHERE artifact_id=?", (artifact_id,))
