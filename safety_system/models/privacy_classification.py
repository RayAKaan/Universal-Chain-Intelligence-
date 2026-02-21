from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PrivacyClassification:
    data_type: str
    sensitivity: str
    retention_days: int
