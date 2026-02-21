from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path


class Database:
    def __init__(self, db_path: str = "uci_capabilities.db"):
        self.db_path = db_path
        self._lock = threading.RLock()
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL;")

    def initialize(self) -> None:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS capabilities (
                    capability_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    version TEXT,
                    capability_type TEXT,
                    category TEXT,
                    subcategory TEXT,
                    state TEXT,
                    health_status TEXT,
                    is_enabled INTEGER,
                    priority_weight REAL,
                    data TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS benchmark_results (
                    result_id TEXT PRIMARY KEY,
                    capability_id TEXT,
                    timestamp TEXT,
                    data TEXT,
                    FOREIGN KEY (capability_id) REFERENCES capabilities(capability_id)
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS state_transitions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    capability_id TEXT,
                    from_state TEXT,
                    to_state TEXT,
                    reason TEXT,
                    timestamp TEXT
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    event_type TEXT,
                    source TEXT,
                    data TEXT,
                    timestamp TEXT
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS discovery_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scanner_name TEXT,
                    timestamp TEXT,
                    capabilities_found INTEGER,
                    errors TEXT,
                    duration_ms REAL
                )
                """
            )
            cur.execute("CREATE INDEX IF NOT EXISTS idx_cap_name_version ON capabilities(name, version)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_cap_type ON capabilities(capability_type)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_cap_category ON capabilities(category)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_cap_state ON capabilities(state)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_cap_enabled ON capabilities(is_enabled)")
            self._conn.commit()

    def execute(self, query: str, params: tuple = ()):
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(query, params)
            self._conn.commit()
            return cur

    def query(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(query, params)
            return cur.fetchall()

    def insert_event(self, event: dict) -> None:
        self.execute(
            "INSERT OR REPLACE INTO events(event_id,event_type,source,data,timestamp) VALUES(?,?,?,?,?)",
            (
                event["event_id"], event["event_type"], event["source"], json.dumps(event["data"], default=str), event["timestamp"],
            ),
        )
