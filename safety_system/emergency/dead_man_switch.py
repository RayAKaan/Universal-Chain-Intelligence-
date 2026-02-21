from datetime import datetime, timezone


class DeadManSwitch:
    def __init__(self):
        self.last_interaction = datetime.now(timezone.utc)

    def reset(self) -> None:
        self.last_interaction = datetime.now(timezone.utc)

    def get_time_since_last_interaction(self) -> float:
        return (datetime.now(timezone.utc) - self.last_interaction).total_seconds()
