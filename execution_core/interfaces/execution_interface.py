"""Standard execution interface for all task handlers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class ExecutionInterface(ABC):
    """Contract for pluggable execution handlers."""

    @abstractmethod
    def execute(self, task_payload: Dict[str, Any]) -> Any:
        """Execute payload and return output."""

    @abstractmethod
    def validate(self, payload: Dict[str, Any]) -> None:
        """Validate payload or raise ValueError."""

    @abstractmethod
    def get_requirements(self) -> Dict[str, Any]:
        """Return required resource metadata for this handler."""
