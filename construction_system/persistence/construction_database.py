from __future__ import annotations
import sqlite3, threading
from pathlib import Path
class ConstructionDatabase:
    def __init__(self,db_path='data/uci_construction.db'):
        Path(db_path).parent.mkdir(parents=True,exist_ok=True)
        self.conn=sqlite3.connect(db_path,check_same_thread=False);self.conn.row_factory=sqlite3.Row;self.conn.execute('PRAGMA journal_mode=WAL;');self.lock=threading.RLock();self.initialize()
    def initialize(self):
        with self.lock:
            c=self.conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS specifications(spec_id TEXT PRIMARY KEY,name TEXT,spec_type TEXT,data TEXT,created_at TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS blueprints(blueprint_id TEXT PRIMARY KEY,spec_id TEXT,name TEXT,status TEXT,data TEXT,created_at TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS artifacts(artifact_id TEXT PRIMARY KEY,name TEXT,artifact_type TEXT,file_path TEXT,checksum TEXT,source_spec_id TEXT,source_blueprint_id TEXT,data TEXT,created_at TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS build_results(result_id TEXT PRIMARY KEY,blueprint_id TEXT,spec_id TEXT,status TEXT,data TEXT,created_at TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS provenance(record_id TEXT PRIMARY KEY,artifact_id TEXT,action TEXT,actor TEXT,data TEXT,timestamp TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS recursive_tasks(task_id TEXT PRIMARY KEY,parent_task_id TEXT,root_task_id TEXT,name TEXT,depth INTEGER,status TEXT,data TEXT,created_at TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS templates(template_id TEXT PRIMARY KEY,name TEXT,template_type TEXT,language TEXT,data TEXT,created_at TEXT)')
            c.execute('CREATE TABLE IF NOT EXISTS components(component_id TEXT PRIMARY KEY,name TEXT,component_type TEXT,blueprint_id TEXT,status TEXT,data TEXT,created_at TEXT)')
            self.conn.commit()
    def execute(self,q,p=()):
        with self.lock:
            cur=self.conn.cursor();cur.execute(q,p);self.conn.commit();return cur
    def query(self,q,p=()):
        with self.lock:
            cur=self.conn.cursor();cur.execute(q,p);return cur.fetchall()
