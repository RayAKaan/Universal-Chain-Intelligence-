from __future__ import annotations
import sqlite3, threading
from pathlib import Path
class OptimizationDatabase:
    def __init__(self,db_path='data/uci_optimization.db'):
        Path(db_path).parent.mkdir(parents=True,exist_ok=True)
        self.conn=sqlite3.connect(db_path,check_same_thread=False);self.conn.row_factory=sqlite3.Row
        self.lock=threading.RLock();self.conn.execute('PRAGMA journal_mode=WAL;');self.initialize()
    def initialize(self):
        stmts=["CREATE TABLE IF NOT EXISTS metrics(metric_id TEXT PRIMARY KEY,name TEXT,metric_type TEXT,source_phase TEXT,source_component TEXT,value REAL,unit TEXT,timestamp TEXT,data TEXT)","CREATE INDEX IF NOT EXISTS idx_metrics_name ON metrics(name)","CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)","CREATE INDEX IF NOT EXISTS idx_metrics_source ON metrics(source_phase,source_component)","CREATE TABLE IF NOT EXISTS bottlenecks(bottleneck_id TEXT PRIMARY KEY,bottleneck_type TEXT,severity TEXT,phase TEXT,component TEXT,status TEXT,data TEXT,first_detected TEXT,last_seen TEXT)","CREATE TABLE IF NOT EXISTS opportunities(opportunity_id TEXT PRIMARY KEY,opportunity_type TEXT,phase TEXT,priority_score REAL,status TEXT,data TEXT,created_at TEXT)","CREATE TABLE IF NOT EXISTS improvements(improvement_id TEXT PRIMARY KEY,improvement_type TEXT,target_phase TEXT,status TEXT,data TEXT,created_at TEXT)","CREATE TABLE IF NOT EXISTS experiments(experiment_id TEXT PRIMARY KEY,experiment_type TEXT,status TEXT,conclusion TEXT,data TEXT,started_at TEXT,completed_at TEXT)","CREATE TABLE IF NOT EXISTS modifications(modification_id TEXT PRIMARY KEY,modification_type TEXT,target_phase TEXT,applied INTEGER,rolled_back INTEGER,data TEXT,created_at TEXT)","CREATE TABLE IF NOT EXISTS campaigns(campaign_id TEXT PRIMARY KEY,name TEXT,status TEXT,data TEXT,started_at TEXT,completed_at TEXT)","CREATE TABLE IF NOT EXISTS baselines(baseline_id TEXT PRIMARY KEY,name TEXT,data TEXT,timestamp TEXT)","CREATE TABLE IF NOT EXISTS optimization_rules(rule_id TEXT PRIMARY KEY,name TEXT,rule_type TEXT,enabled INTEGER,data TEXT,created_at TEXT)","CREATE TABLE IF NOT EXISTS knowledge_patterns(pattern_id TEXT PRIMARY KEY,pattern_type TEXT,data TEXT,created_at TEXT)","CREATE TABLE IF NOT EXISTS cycle_results(cycle_id TEXT PRIMARY KEY,data TEXT,timestamp TEXT)","CREATE TABLE IF NOT EXISTS improvement_events(event_id TEXT PRIMARY KEY,improvement_id TEXT,event_type TEXT,data TEXT,timestamp TEXT)"]
        with self.lock:
            for s in stmts:self.conn.execute(s)
            self.conn.commit()
    def execute(self,sql,params=()):
        with self.lock:
            cur=self.conn.execute(sql,params);self.conn.commit();return cur
    def query(self,sql,params=()):
        with self.lock:return self.conn.execute(sql,params).fetchall()
