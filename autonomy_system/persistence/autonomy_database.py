from __future__ import annotations
import sqlite3, threading
from pathlib import Path
class AutonomyDatabase:
    def __init__(self,db_path='data/uci_autonomy.db'):
        Path(db_path).parent.mkdir(parents=True,exist_ok=True)
        self.conn=sqlite3.connect(db_path,check_same_thread=False); self.conn.row_factory=sqlite3.Row
        self.lock=threading.RLock(); self.conn.execute('PRAGMA journal_mode=WAL;'); self.initialize()
    def initialize(self):
        stmts=["CREATE TABLE IF NOT EXISTS system_state(state_id TEXT PRIMARY KEY,status TEXT,autonomy_level TEXT,data TEXT,timestamp TEXT)","CREATE TABLE IF NOT EXISTS goal_records(record_id TEXT PRIMARY KEY,source TEXT,raw_input TEXT,goal_id TEXT,plan_id TEXT,priority INTEGER,status TEXT,tenant_id TEXT,data TEXT,submitted_at TEXT,started_at TEXT,completed_at TEXT)","CREATE INDEX IF NOT EXISTS idx_goals_status ON goal_records(status)","CREATE INDEX IF NOT EXISTS idx_goals_submitted ON goal_records(submitted_at)","CREATE TABLE IF NOT EXISTS acquisition_records(acquisition_id TEXT PRIMARY KEY,name TEXT,acquisition_type TEXT,status TEXT,data TEXT,started_at TEXT,completed_at TEXT)","CREATE TABLE IF NOT EXISTS healing_events(event_id TEXT PRIMARY KEY,failure_type TEXT,affected_phase TEXT,severity TEXT,recovery_success INTEGER,data TEXT,detection_time TEXT,recovery_time TEXT)","CREATE TABLE IF NOT EXISTS learning_records(record_id TEXT PRIMARY KEY,learning_type TEXT,confidence REAL,data TEXT,created_at TEXT,applied_count INTEGER,last_applied TEXT)","CREATE INDEX IF NOT EXISTS idx_learning_type ON learning_records(learning_type)","CREATE TABLE IF NOT EXISTS knowledge_entries(entry_id TEXT PRIMARY KEY,knowledge_type TEXT,subject TEXT,predicate TEXT,object TEXT,confidence REAL,source TEXT,data TEXT,created_at TEXT,updated_at TEXT)","CREATE INDEX IF NOT EXISTS idx_knowledge_subject ON knowledge_entries(subject)","CREATE INDEX IF NOT EXISTS idx_knowledge_type ON knowledge_entries(knowledge_type)","CREATE TABLE IF NOT EXISTS telemetry(point_id TEXT PRIMARY KEY,category TEXT,name TEXT,value REAL,unit TEXT,source_phase TEXT,dimensions TEXT,timestamp TEXT)","CREATE INDEX IF NOT EXISTS idx_telemetry_time ON telemetry(timestamp)","CREATE INDEX IF NOT EXISTS idx_telemetry_category ON telemetry(category)","CREATE TABLE IF NOT EXISTS autonomy_decisions(decision_id TEXT PRIMARY KEY,action TEXT,autonomy_level TEXT,auto_approved INTEGER,data TEXT,timestamp TEXT)","CREATE TABLE IF NOT EXISTS runtime_events(event_id TEXT PRIMARY KEY,event_type TEXT,data TEXT,timestamp TEXT)","CREATE TABLE IF NOT EXISTS communication_log(message_id TEXT PRIMARY KEY,direction TEXT,protocol TEXT,message_type TEXT,data TEXT,timestamp TEXT)"]
        with self.lock:
            for s in stmts: self.conn.execute(s)
            self.conn.commit()
    def execute(self,sql,params=()):
        with self.lock:
            c=self.conn.execute(sql,params); self.conn.commit(); return c
    def query(self,sql,params=()):
        with self.lock: return self.conn.execute(sql,params).fetchall()
