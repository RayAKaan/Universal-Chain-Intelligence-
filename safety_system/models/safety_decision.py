from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class ActionClassification(str, Enum):
    SAFE = "SAFE"
    CAUTION = "CAUTION"
    RISKY = "RISKY"
    DANGEROUS = "DANGEROUS"
    FORBIDDEN = "FORBIDDEN"


class RiskLevel(int, Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    UNACCEPTABLE = 5


@dataclass(frozen=True)
class ConstitutionalCheck:
    passed: bool
    principles_checked: list[str]
    violations: list[str]


@dataclass(frozen=True)
class HarmAssessmentSummary:
    potential_harms: list[str]
    harm_probability: float
    harm_severity: str
    affected_parties: list[str]
    reversible: bool


@dataclass
class SafetyDecision:
    action_requested: str
    action_source: str
    action_target: str
    classification: ActionClassification
    risk_level: RiskLevel
    constitutional_check: ConstitutionalCheck
    harm_assessment: HarmAssessmentSummary
    consent_required: bool = False
    consent_obtained: bool = False
    consent_record_id: str = ""
    trust_level_required: str = "probationary"
    current_trust_level: str = "probationary"
    trust_sufficient: bool = False
    containment_check: bool = True
    scope_check: bool = True
    rate_limit_check: bool = True
    decision: str = "deny"
    conditions: list[str] = field(default_factory=list)
    reasoning: str = ""
    override_by_human: bool = False
    human_override_reason: str = ""
    metadata: dict = field(default_factory=dict)
    decision_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
