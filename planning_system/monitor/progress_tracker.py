from __future__ import annotations

import time


class ProgressTracker:
    def __init__(self):
        self.events: dict[str, list[dict]] = {}

    def track(self, plan_id, step_id, status, result=None):
        self.events.setdefault(plan_id, []).append({"ts": time.time(), "step_id": step_id, "status": status, "result": result})

    def get_progress(self, plan_id):
        ev = self.events.get(plan_id, [])
        counts = {}
        for e in ev:
            counts[e["status"]] = counts.get(e["status"], 0) + 1
        return counts

    def get_step_history(self, plan_id):
        return self.events.get(plan_id, [])

    def estimate_remaining(self, plan_id):
        ev = self.events.get(plan_id, [])
        durations = []
        start = {}
        for e in ev:
            if e["status"] == "RUNNING":
                start[e["step_id"]] = e["ts"]
            if e["status"] in {"COMPLETED", "FAILED"} and e["step_id"] in start:
                durations.append((e["ts"] - start[e["step_id"]]) * 1000)
        return sum(durations) / len(durations) if durations else 0.0
