class ScopeMonitor:
    def __init__(self):
        self.events = []

    def record(self, action: str, ok: bool, reason: str) -> None:
        self.events.append({"action": action, "ok": ok, "reason": reason})

    def recent(self, limit: int = 20) -> list[dict]:
        return self.events[-limit:]
