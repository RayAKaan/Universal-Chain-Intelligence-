"""Deterministic-safe task id generation utilities."""

from __future__ import annotations

import itertools
import threading
from datetime import datetime, timezone

_counter = itertools.count(1)
_lock = threading.Lock()


def generate_task_id(prefix: str = "task") -> str:
    """Generate a monotonic identifier with UTC timestamp and sequence."""
    with _lock:
        sequence = next(_counter)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}-{timestamp}-{sequence:06d}"
