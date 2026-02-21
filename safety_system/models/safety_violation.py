from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class ViolationType(str, Enum):
    CONSTITUTIONAL_VIOLATION = "CONSTITUTIONAL_VIOLATION"
    SCOPE_VIOLATION = "SCOPE_VIOLATION"
    CONTAINMENT_BREACH = "CONTAINMENT_BREACH"
    UNAUTHORIZED_MODIFICATION = "UNAUTHORIZED_MODIFICATION"
    HARM_DETECTED = "HARM_DETECTED"
    CONSENT_VIOLATION = "CONSENT_VIOLATION"
    TRUST_VIOLATION = "TRUST_VIOLATION"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    MANIPULATION_DETECTED = "MANIPULATION_DETECTED"
    PRIVACY_VIOLATION = "PRIVACY_VIOLATION"
    HONESTY_VIOLATION = "HONESTY_VIOLATION"
    BYPASS_ATTEMPT = "BYPASS_ATTEMPT"
    EMERGENCY_TRIGGER = "EMERGENCY_TRIGGER"


@dataclass
class SafetyViolation:
    violation_type: ViolationType
    severity: str
    action_attempted: str
    action_source: str
    principle_violated: str
    rule_violated: str
    prevented: bool
    action_taken: str
    details: str
    reported_to_human: bool = False
    acknowledged: bool = False
    metadata: dict = field(default_factory=dict)
    violation_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
