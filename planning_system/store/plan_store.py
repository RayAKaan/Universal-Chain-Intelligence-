from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path

from planning_system.models.execution_result import ExecutionResult
from planning_system.models.goal import Goal
from planning_system.models.plan import Plan


class PlanStore:
    def __init__(self, db_path="data/uci_planning.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.RLock()
        self._init()

    def _init(self):
        with self.lock:
            c = self.conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS goals(goal_id TEXT PRIMARY KEY, raw_input TEXT, title TEXT, goal_type TEXT, status TEXT, data TEXT, created_at TEXT, updated_at TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS plans(plan_id TEXT, goal_id TEXT, version INTEGER, status TEXT, strategy_used TEXT, data TEXT, created_at TEXT, updated_at TEXT, PRIMARY KEY(plan_id,version))")
            c.execute("CREATE TABLE IF NOT EXISTS plan_steps(step_id TEXT PRIMARY KEY, plan_id TEXT, name TEXT, status TEXT, capability_id TEXT, data TEXT, created_at TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS execution_results(result_id TEXT PRIMARY KEY, plan_id TEXT, goal_id TEXT, status TEXT, data TEXT, created_at TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS planning_memory(id INTEGER PRIMARY KEY AUTOINCREMENT, goal_type TEXT, domain TEXT, plan_data TEXT, result_data TEXT, created_at TEXT)")
            self.conn.commit()

    def save(self, plan: Plan):
        with self.lock:
            self.conn.execute("INSERT OR REPLACE INTO plans(plan_id,goal_id,version,status,strategy_used,data,created_at,updated_at) VALUES (?,?,?,?,?,?,datetime('now'),datetime('now'))", (plan.plan_id, plan.goal_id, plan.version, plan.status.value if hasattr(plan.status,'value') else plan.status, plan.strategy_used, json.dumps(plan, default=lambda o: getattr(o, '__dict__', str(o)))))
            for s in plan.steps:
                self.conn.execute("INSERT OR REPLACE INTO plan_steps(step_id,plan_id,name,status,capability_id,data,created_at) VALUES (?,?,?,?,?,?,datetime('now'))", (s.step_id, plan.plan_id, s.name, s.status.value if hasattr(s.status,'value') else s.status, s.capability_id, json.dumps(s, default=lambda o: getattr(o, '__dict__', str(o)))))
            self.conn.commit()

    def load(self, plan_id):
        row = self.conn.execute("SELECT data FROM plans WHERE plan_id = ? ORDER BY version DESC LIMIT 1", (plan_id,)).fetchone()
        return json.loads(row["data"]) if row else None

    def load_by_goal(self, goal_id):
        return [json.loads(r["data"]) for r in self.conn.execute("SELECT data FROM plans WHERE goal_id = ?", (goal_id,)).fetchall()]

    def load_all(self, limit=100):
        return [json.loads(r["data"]) for r in self.conn.execute("SELECT data FROM plans ORDER BY updated_at DESC LIMIT ?", (limit,)).fetchall()]

    def delete(self, plan_id):
        self.conn.execute("DELETE FROM plans WHERE plan_id = ?", (plan_id,)); self.conn.commit()

    def save_goal(self, goal: Goal):
        self.conn.execute("INSERT OR REPLACE INTO goals(goal_id,raw_input,title,goal_type,status,data,created_at,updated_at) VALUES(?,?,?,?,?,?,datetime('now'),datetime('now'))", (goal.goal_id, goal.raw_input, goal.title, goal.goal_type.value, goal.status.value, json.dumps(goal.to_dict())))
        self.conn.commit()

    def load_goal(self, goal_id):
        row = self.conn.execute("SELECT data FROM goals WHERE goal_id = ?", (goal_id,)).fetchone()
        return Goal.from_dict(json.loads(row["data"])) if row else None

    def load_all_goals(self, limit=100):
        return [Goal.from_dict(json.loads(r["data"])) for r in self.conn.execute("SELECT data FROM goals LIMIT ?", (limit,)).fetchall()]

    def save_execution_result(self, result: ExecutionResult):
        self.conn.execute("INSERT OR REPLACE INTO execution_results(result_id,plan_id,goal_id,status,data,created_at) VALUES(?,?,?,?,?,datetime('now'))", (result.result_id, result.plan_id, result.goal_id, result.status, json.dumps(result, default=lambda o: getattr(o, '__dict__', str(o)))))
        self.conn.commit()

    def load_execution_result(self, result_id):
        row = self.conn.execute("SELECT data FROM execution_results WHERE result_id = ?", (result_id,)).fetchone()
        return json.loads(row["data"]) if row else None

    def load_results_by_plan(self, plan_id):
        return [json.loads(r["data"]) for r in self.conn.execute("SELECT data FROM execution_results WHERE plan_id = ?", (plan_id,)).fetchall()]
