from __future__ import annotations

from datetime import datetime, timedelta, timezone

from capability_system.models.benchmark_result import BenchmarkResult
from capability_system.persistence.database import Database
from capability_system.persistence.serialization import deserialize_benchmark_result, serialize_benchmark_result


class BenchmarkStore:
    def __init__(self, database: Database):
        self.db = database

    def save(self, result: BenchmarkResult) -> None:
        self.db.execute("INSERT OR REPLACE INTO benchmark_results(result_id, capability_id, timestamp, data) VALUES (?,?,?,?)", (result.result_id, result.capability_id, result.timestamp.isoformat(), serialize_benchmark_result(result)))

    def load(self, result_id: str) -> BenchmarkResult:
        rows = self.db.query("SELECT data FROM benchmark_results WHERE result_id = ?", (result_id,))
        if not rows:
            raise KeyError(result_id)
        return deserialize_benchmark_result(rows[0]["data"])

    def load_by_capability(self, capability_id: str) -> list[BenchmarkResult]:
        return [deserialize_benchmark_result(r["data"]) for r in self.db.query("SELECT data FROM benchmark_results WHERE capability_id = ? ORDER BY timestamp", (capability_id,))]

    def load_latest(self, capability_id: str) -> BenchmarkResult | None:
        rows = self.db.query("SELECT data FROM benchmark_results WHERE capability_id = ? ORDER BY timestamp DESC LIMIT 1", (capability_id,))
        return deserialize_benchmark_result(rows[0]["data"]) if rows else None

    def load_all(self) -> list[BenchmarkResult]:
        return [deserialize_benchmark_result(r["data"]) for r in self.db.query("SELECT data FROM benchmark_results")]

    def purge_old(self, days: int = 90) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        cur = self.db.execute("DELETE FROM benchmark_results WHERE timestamp < ?", (cutoff.isoformat(),))
        return cur.rowcount
