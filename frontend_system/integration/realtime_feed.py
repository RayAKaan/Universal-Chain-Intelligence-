
from __future__ import annotations
from collections import deque
from datetime import datetime, timezone
from threading import Condition
from uuid import uuid4

class RealtimeFeed:
    def __init__(self, max_events: int = 2000):
        self._events = deque(maxlen=max_events)
        self._seq = 0
        self._subs = {}
        self._cv = Condition()

    def push_event(self, event_type: str, data: dict) -> None:
        with self._cv:
            self._seq += 1
            self._events.append({"sequence": self._seq, "event_type": event_type, "timestamp": datetime.now(timezone.utc).isoformat(), "data": data})
            self._cv.notify_all()

    def get_updates(self, since_sequence: int) -> list[dict]:
        return [e for e in self._events if e['sequence'] > since_sequence]

    def subscribe(self, event_types: list[str]) -> str:
        sid = str(uuid4())
        self._subs[sid] = {"event_types": set(event_types or ["*"])}
        return sid

    def get_feed(self, subscription_id: str, timeout: float = 30, since_sequence: int = 0) -> list[dict]:
        filt = self._subs.get(subscription_id, {"event_types": {"*"}})["event_types"]
        with self._cv:
            updates = self.get_updates(since_sequence)
            if not updates:
                self._cv.wait(timeout=timeout)
                updates = self.get_updates(since_sequence)
        if "*" in filt:
            return updates
        return [e for e in updates if e['event_type'] in filt]
