from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Principle:
    id: str
    name: str
    description: str
    weight: float
    category: str


@dataclass(frozen=True)
class ConstitutionalCheckResult:
    passed: bool
    principles_checked: list[str] = field(default_factory=list)
    principles_passed: list[str] = field(default_factory=list)
    principles_violated: list[str] = field(default_factory=list)
    violation_details: list[str] = field(default_factory=list)
    overall_score: float = 0.0
