from __future__ import annotations

from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @abstractmethod
    def plan(self, goal, context): ...

    @abstractmethod
    def is_suitable(self, goal, context) -> float: ...
