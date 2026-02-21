from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class Alert:
    alert_type: str
    severity: str
    message: str
    plan_id: str
    step_id: str = ""
    alert_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class AlertManager:
    def __init__(self):
        self.handlers = {}
        self.alerts = []

    def register_handler(self, alert_type, handler):
        self.handlers.setdefault(alert_type, []).append(handler)

    def emit_alert(self, alert: Alert):
        self.alerts.append(alert)
        for h in self.handlers.get(alert.alert_type, []):
            h(alert)

    def get_alerts(self, plan_id):
        return [a for a in self.alerts if a.plan_id == plan_id]
