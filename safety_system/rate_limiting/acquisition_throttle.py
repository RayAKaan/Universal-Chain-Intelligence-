from collections import deque
from datetime import datetime, timezone


class AcquisitionThrottle:
    def __init__(self):
        self.events = deque()

    def allow(self, per_hour: int = 5) -> tuple[bool, str]:
        now = datetime.now(timezone.utc).timestamp()
        while self.events and self.events[0] < now - 3600:
            self.events.popleft()
        if len(self.events) >= per_hour:
            return False, "acquisition hourly limit reached"
        self.events.append(now)
        return True, "ok"
