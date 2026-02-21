"""Task abstraction for deterministic execution."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from execution_core.utils.id_generator import generate_task_id


@dataclass(order=True)
class Task:
    """Serializable task model with execution lifecycle state."""

    sort_index: tuple[int, str] = field(init=False, repr=False)
    priority: int
    task_type: str
    payload: Dict[str, Any]
    task_id: str = field(default_factory=generate_task_id)
    status: str = field(default="pending", compare=False)
    result: Optional[Any] = field(default=None, compare=False)
    error: Optional[str] = field(default=None, compare=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc), compare=False)
    started_at: Optional[datetime] = field(default=None, compare=False)
    completed_at: Optional[datetime] = field(default=None, compare=False)

    def __post_init__(self) -> None:
        self.sort_index = (self.priority, self.task_id)

    def execute(self) -> None:
        """Compatibility no-op; actual execution is delegated to engine handlers."""
        self.mark_running()

    def mark_running(self) -> None:
        self.status = "running"
        self.started_at = datetime.now(timezone.utc)

    def mark_completed(self, result: Any) -> None:
        self.status = "completed"
        self.result = result
        self.error = None
        self.completed_at = datetime.now(timezone.utc)

    def mark_failed(self, error: Exception | str) -> None:
        self.status = "failed"
        self.error = str(error)
        self.completed_at = datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        for key in ("created_at", "started_at", "completed_at"):
            value = data[key]
            data[key] = value.isoformat() if value else None
        data.pop("sort_index", None)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        clone = dict(data)
        for key in ("created_at", "started_at", "completed_at"):
            value = clone.get(key)
            clone[key] = datetime.fromisoformat(value) if value else None
        return cls(**clone)
