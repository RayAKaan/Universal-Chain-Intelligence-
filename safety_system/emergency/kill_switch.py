from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


class KillSwitch:
    def __init__(self, state_file: str = "data/.kill_switch"):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.activated = self.state_file.exists()
        self.activated_at = None
        self.activated_by = None

    def activate(self, by: str = "human") -> None:
        if by != "human":
            raise PermissionError("kill switch is human-only")
        self.activated = True
        self.activated_at = datetime.now(timezone.utc)
        self.activated_by = by
        self.state_file.write_text("activated")

    def deactivate(self, authorization: str) -> None:
        if authorization != "human_authorized":
            raise PermissionError("human authorization required")
        self.activated = False
        if self.state_file.exists():
            self.state_file.unlink()

    def is_activated(self) -> bool:
        return self.activated
