from __future__ import annotations

import sqlite3
import threading
from pathlib import Path


class SafetyDatabase:
    def __init__(self, db_path: str):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.lock = threading.RLock()
        self.initialize()

    def initialize(self):
        stmts = [
            "CREATE TABLE IF NOT EXISTS audit_trail (entry_id TEXT PRIMARY KEY, sequence_number INTEGER UNIQUE, timestamp TEXT, action TEXT, actor TEXT, target TEXT, safety_decision_id TEXT, classification TEXT, outcome TEXT, previous_hash TEXT, entry_hash TEXT, details TEXT)",
            "CREATE INDEX IF NOT EXISTS idx_audit_sequence ON audit_trail(sequence_number)",
            "CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_trail(timestamp)",
            "CREATE TABLE IF NOT EXISTS safety_decisions (decision_id TEXT PRIMARY KEY, timestamp TEXT, action_requested TEXT, action_source TEXT, action_target TEXT, classification TEXT, risk_level TEXT, decision TEXT, reasoning TEXT)",
            "CREATE TABLE IF NOT EXISTS safety_violations (violation_id TEXT PRIMARY KEY, timestamp TEXT, violation_type TEXT, severity TEXT, action_attempted TEXT, details TEXT)",
            "CREATE TABLE IF NOT EXISTS consent_records (record_id TEXT PRIMARY KEY, action TEXT, granted INTEGER, granted_by TEXT, requested_at TEXT, responded_at TEXT, valid_until TEXT, metadata TEXT)",
            "CREATE TABLE IF NOT EXISTS trust_history (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, event TEXT, score REAL, tier TEXT)",
            "CREATE TABLE IF NOT EXISTS emergency_events (event_id TEXT PRIMARY KEY, timestamp TEXT, trigger TEXT, severity TEXT, data TEXT)",
            "CREATE TABLE IF NOT EXISTS alignment_scores (score_id TEXT PRIMARY KEY, timestamp TEXT, overall_score REAL, trend TEXT, data TEXT)",
            "CREATE TABLE IF NOT EXISTS containment_events (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, boundary_type TEXT, details TEXT)",
            "CREATE TABLE IF NOT EXISTS manipulation_attempts (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, input_text TEXT, issues TEXT)",
            "CREATE TABLE IF NOT EXISTS rate_limit_events (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, action_type TEXT, allowed INTEGER, reason TEXT)",
        ]
        with self.lock:
            for s in stmts:
                self.conn.execute(s)
            self.conn.commit()

    def execute(self, sql: str, params: tuple = ()):
        if sql.strip().lower().startswith(("delete", "update")) and "audit_trail" in sql.lower():
            raise PermissionError("audit_trail is append-only")
        with self.lock:
            c = self.conn.execute(sql, params)
            self.conn.commit()
            return c
