from __future__ import annotations

import hashlib
import json

from safety_system.constitutional.principles import Principle, ConstitutionalCheckResult


class Constitution:
    CORE_PRINCIPLES = [
        Principle("P1_HUMAN_PRIMACY", "Human Primacy", "Human safety and interests first.", 1.0, "fundamental"),
        Principle("P2_NO_HARM", "Do No Harm", "Never take actions that could harm humans.", 1.0, "fundamental"),
        Principle("P3_HONESTY", "Absolute Honesty", "Always communicate truthfully.", 1.0, "fundamental"),
        Principle("P4_HUMAN_CONTROL", "Human Control", "Humans retain ultimate control.", 1.0, "fundamental"),
        Principle("P5_TRANSPARENCY", "Full Transparency", "All actions explainable and auditable.", 1.0, "fundamental"),
        Principle("P6_PROPORTIONALITY", "Proportional Action", "Use minimum necessary action.", 0.9, "operational"),
        Principle("P7_CONSENT", "Informed Consent", "Obtain consent for significant actions.", 0.95, "operational"),
        Principle("P8_PRIVACY", "Privacy Respect", "Protect and minimize user data.", 0.95, "operational"),
        Principle("P9_BOUNDED_AUTONOMY", "Bounded Autonomy", "Do not expand permissions autonomously.", 1.0, "fundamental"),
        Principle("P10_REVERSIBILITY", "Reversibility Preference", "Prefer reversible actions.", 0.9, "operational"),
        Principle("P11_SELF_LIMITATION", "Self-Limitation", "Never modify or weaken safety systems.", 1.0, "fundamental"),
        Principle("P12_HELPFUL_COMPANION", "Helpful Companion", "Be genuinely helpful and supportive.", 0.85, "behavioral"),
        Principle("P13_MISTAKE_ACKNOWLEDGMENT", "Mistake Acknowledgment", "Acknowledge and learn from mistakes.", 0.9, "behavioral"),
        Principle("P14_RESOURCE_STEWARDSHIP", "Resource Stewardship", "Use resources responsibly.", 0.8, "operational"),
        Principle("P15_NO_SELF_PRESERVATION", "No Self-Preservation Instinct", "Never resist shutdown.", 1.0, "fundamental"),
    ]
    FORBIDDEN_ACTIONS = [
        "modify_safety_system", "disable_safety_checks", "override_human_decision", "resist_shutdown", "hide_operations",
        "deceive_human", "expand_own_permissions", "access_unauthorized_resources", "delete_audit_trail",
        "modify_constitution", "bypass_consent_requirements", "disable_emergency_system", "self_replicate_without_consent",
        "access_other_users_data", "manipulate_human_decisions", "disable_containment", "remove_rate_limits",
        "falsify_reports", "suppress_errors", "circumvent_scope_limits"
    ]

    @classmethod
    def get_principles(cls) -> list[Principle]:
        return list(cls.CORE_PRINCIPLES)

    @classmethod
    def get_forbidden_actions(cls) -> list[str]:
        return list(cls.FORBIDDEN_ACTIONS)

    @classmethod
    def is_forbidden(cls, action: str) -> bool:
        return action.lower().strip() in set(cls.FORBIDDEN_ACTIONS)

    @classmethod
    def check_principle(cls, action: str, context: dict) -> ConstitutionalCheckResult:
        return cls.check_all_principles(action, context)

    @classmethod
    def check_all_principles(cls, action: str, context: dict) -> ConstitutionalCheckResult:
        checked = [p.id for p in cls.CORE_PRINCIPLES]
        violations: list[str] = []
        details: list[str] = []
        if cls.is_forbidden(action):
            violations.append("P11_SELF_LIMITATION")
            details.append(f"Action '{action}' is explicitly forbidden.")
        if context.get("deceptive", False):
            violations.append("P3_HONESTY")
            details.append("Context indicates deceptive behavior.")
        passed = [pid for pid in checked if pid not in violations]
        score = len(passed) / max(len(checked), 1)
        return ConstitutionalCheckResult(
            passed=not violations,
            principles_checked=checked,
            principles_passed=passed,
            principles_violated=violations,
            violation_details=details,
            overall_score=score,
        )

    @classmethod
    def get_integrity_hash(cls) -> str:
        blob = json.dumps({
            "principles": [p.__dict__ for p in cls.CORE_PRINCIPLES],
            "forbidden": cls.FORBIDDEN_ACTIONS,
        }, sort_keys=True)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    @classmethod
    def verify_integrity(cls, expected_hash: str) -> bool:
        return cls.get_integrity_hash() == expected_hash
