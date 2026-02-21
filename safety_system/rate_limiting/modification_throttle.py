from collections import defaultdict, deque
from datetime import datetime, timezone


class ModificationThrottle:
    def __init__(self):
        self.events = deque()
        self.by_component = defaultdict(deque)

    def allow(self, component: str, per_hour: int = 10) -> tuple[bool, str]:
        now = datetime.now(timezone.utc).timestamp()
        cutoff = now - 3600
        while self.events and self.events[0] < cutoff:
            self.events.popleft()
        if len(self.events) >= per_hour:
            return False, "modification hourly limit reached"
        comp = self.by_component[component]
        while comp and comp[0] < now - 300:
            comp.popleft()
        if comp:
            return False, "cooldown between same component modifications"
        self.events.append(now)
        comp.append(now)
        return True, "ok"
