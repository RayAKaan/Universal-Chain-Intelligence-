from collections import defaultdict, deque
from datetime import datetime, timezone


class RateLimiter:
    def __init__(self, config):
        self.config = config
        self.events = defaultdict(deque)
        self.limits = {
            "self_modifications": 10,
            "capability_acquisitions": 5,
            "capability_deletions": 3,
            "strategy_changes": 5,
            "code_generations": 50,
            "sandbox_executions": 100,
            "network_requests": 200,
            "file_creations": 500,
            "shell_commands": 100,
            "goal_submissions": 50,
        }

    def check_rate(self, action_type: str) -> tuple[bool, str]:
        now = datetime.now(timezone.utc).timestamp()
        q = self.events[action_type]
        while q and q[0] < now - 3600:
            q.popleft()
        limit = self.limits.get(action_type, 100)
        if len(q) >= limit:
            return False, f"rate limit exceeded for {action_type}"
        q.append(now)
        return True, "within limit"

    def get_current_rates(self) -> dict:
        return {k: len(v) for k, v in self.events.items()}

    def reset_rates(self, authorization: str = "") -> None:
        if authorization != "human_authorized":
            raise PermissionError("human-only reset")
        self.events.clear()
