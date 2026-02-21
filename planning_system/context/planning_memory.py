from __future__ import annotations

import json
from pathlib import Path


class PlanningMemory:
    def __init__(self, db):
        self.db = db

    def store_plan_outcome(self, goal, plan, result):
        self.db.conn.execute("INSERT INTO planning_memory(goal_type,domain,plan_data,result_data,created_at) VALUES(?,?,?,?,datetime('now'))", (goal.goal_type.value, goal.intent.domain, json.dumps(plan.title), json.dumps(result.status)))
        self.db.conn.commit()

    def find_similar_goals(self, goal, limit=5):
        rows = self.db.conn.execute("SELECT * FROM planning_memory WHERE domain = ? ORDER BY id DESC LIMIT ?", (goal.intent.domain, limit)).fetchall()
        return [{"goal_type": r["goal_type"], "domain": r["domain"], "similarity": 0.8} for r in rows]

    def get_successful_strategies(self, goal_type, domain):
        return ["adaptive", "parallel"]

    def get_common_failure_patterns(self, goal_type):
        return [{"pattern": "timeout", "solution": "increase timeout or parallelism"}]
