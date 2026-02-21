from datetime import datetime, timezone


class EscalationManager:
    def __init__(self):
        self._history = []
        self._pending = []

    def escalate(self, action: str, reason: str, severity: str) -> None:
        item = {"time": datetime.now(timezone.utc).isoformat(), "action": action, "reason": reason, "severity": severity}
        self._history.append(item)
        self._pending.append(item)

    def get_escalation_history(self) -> list[dict]:
        return list(self._history)

    def get_pending_escalations(self) -> list[dict]:
        return list(self._pending)
