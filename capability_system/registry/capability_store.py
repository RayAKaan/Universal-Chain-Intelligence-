from __future__ import annotations

import shutil

from capability_system.models.capability import Capability
from capability_system.persistence.database import Database
from capability_system.persistence.serialization import deserialize_capability, serialize_capability


class CapabilityStore:
    def __init__(self, database: Database):
        self.db = database

    def save(self, capability: Capability) -> None:
        payload = serialize_capability(capability)
        self.db.execute(
            """
            INSERT OR REPLACE INTO capabilities(capability_id,name,version,capability_type,category,subcategory,state,health_status,is_enabled,priority_weight,data,created_at,updated_at)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                capability.capability_id,
                capability.name,
                capability.version,
                capability.capability_type.value,
                capability.category,
                capability.subcategory,
                capability.state.value,
                capability.health_status.value,
                int(capability.is_enabled),
                capability.priority_weight,
                payload,
                capability.created_at.isoformat(),
                capability.updated_at.isoformat(),
            ),
        )

    def load(self, capability_id: str) -> Capability:
        rows = self.db.query("SELECT data FROM capabilities WHERE capability_id = ?", (capability_id,))
        if not rows:
            raise KeyError(capability_id)
        return deserialize_capability(rows[0]["data"])

    def load_all(self) -> list[Capability]:
        return [deserialize_capability(r["data"]) for r in self.db.query("SELECT data FROM capabilities")]

    def delete(self, capability_id: str) -> None:
        self.db.execute("DELETE FROM capabilities WHERE capability_id = ?", (capability_id,))

    def search(self, query: dict) -> list[Capability]:
        clauses, params = [], []
        for k, v in query.items():
            clauses.append(f"{k} = ?")
            params.append(v)
        sql = "SELECT data FROM capabilities"
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        return [deserialize_capability(r["data"]) for r in self.db.query(sql, tuple(params))]

    def backup(self, path: str) -> None:
        shutil.copy2(self.db.db_path, path)

    def restore(self, path: str) -> None:
        shutil.copy2(path, self.db.db_path)
