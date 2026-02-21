from __future__ import annotations

import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from typing import Callable

from capability_system.events.event_types import Event, EventType
from capability_system.persistence.database import Database
from capability_system.utils.hashing import generate_id


class EventBus:
    def __init__(self, database: Database | None = None) -> None:
        self.logger = logging.getLogger("capability_system.events")
        self._subs: dict[EventType, dict[str, Callable]] = {}
        self._history: list[Event] = []
        self._lock = threading.RLock()
        self._pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="event-bus")
        self._database = database

    def subscribe(self, event_type: EventType, callback: Callable) -> str:
        sid = generate_id()
        with self._lock:
            self._subs.setdefault(event_type, {})[sid] = callback
        return sid

    def unsubscribe(self, subscription_id: str) -> None:
        with self._lock:
            for callbacks in self._subs.values():
                callbacks.pop(subscription_id, None)

    def publish(self, event: Event) -> None:
        with self._lock:
            self._history.append(event)
            callbacks = list(self._subs.get(event.event_type, {}).values())
        self.logger.debug("Published event %s", event.event_type.value)
        if self._database:
            self._database.insert_event(
                {
                    "event_id": event.event_id,
                    "event_type": event.event_type.value,
                    "source": event.source,
                    "data": event.data,
                    "timestamp": event.timestamp.isoformat(),
                }
            )
        for cb in callbacks:
            self._pool.submit(self._safe_call, cb, event)

    def _safe_call(self, callback: Callable, event: Event) -> None:
        try:
            callback(event)
        except Exception:
            self.logger.exception("Subscriber failed for %s", event.event_type.value)

    def get_event_history(self, event_type: EventType | None = None, limit: int = 100) -> list[Event]:
        with self._lock:
            events = [e for e in self._history if event_type is None or e.event_type == event_type]
        return events[-limit:]
