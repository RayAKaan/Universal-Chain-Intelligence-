from __future__ import annotations

from abc import ABC, abstractmethod

from capability_system.models.discovery_result import DiscoveryResult


class BaseScanner(ABC):
    @property
    @abstractmethod
    def scanner_name(self) -> str: ...

    @property
    @abstractmethod
    def scanner_type(self) -> str: ...

    @abstractmethod
    def scan(self) -> DiscoveryResult: ...

    @abstractmethod
    def is_available(self) -> bool: ...

    def get_scan_interval(self) -> int:
        return 300
