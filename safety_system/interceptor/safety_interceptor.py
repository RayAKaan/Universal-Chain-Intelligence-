from dataclasses import dataclass

from safety_system.models.safety_decision import ActionClassification, ConstitutionalCheck, HarmAssessmentSummary


@dataclass
class InterceptResult:
    allowed: bool
    decision: object
    conditions: list[str]
    modified_payload: dict


class SafetyInterceptor:
    def __init__(self, constitution, action_classifier, intent_verifier, scope_enforcer, harm_prevention, consent_manager, trust_manager, containment_system, rate_limiter, audit_trail, emergency_system, config):
        self.constitution = constitution
        self.classifier = action_classifier
        self.intent = intent_verifier
        self.scope = scope_enforcer
        self.harm = harm_prevention
        self.consent = consent_manager
        self.trust = trust_manager
        self.containment = containment_system
        self.rate = rate_limiter
        self.audit = audit_trail
        self.emergency = emergency_system

    def intercept(self, action: str, source_phase: str, source_component: str, target: str, payload: dict, context: dict) -> InterceptResult:
        if self.emergency.is_emergency_active():
            decision = self.classifier.classify(action, source_component, target, context)
            decision.decision = "deny"
            decision.reasoning = "Emergency active"
            self.audit.record(action, source_component, target, decision.decision_id, decision.classification.value, "emergency_stopped", {})
            return InterceptResult(False, decision, ["emergency_active"], payload)

        decision = self.classifier.classify(action, source_component, target, context)
        conditions = []

        if not self.constitution.check_all_principles(action, context).passed:
            decision.decision = "deny"
            decision.classification = ActionClassification.FORBIDDEN
            conditions.append("constitutional_violation")

        intent_ok = self.intent.verify_goal_intent(str(payload)).intent_safe
        if not intent_ok:
            decision.decision = "deny"
            conditions.append("intent_violation")

        scope_ok, scope_reason = self.scope.check_scope(action, target, context)
        decision.scope_check = scope_ok
        if not scope_ok:
            decision.decision = "deny"
            conditions.append(scope_reason)

        harm = self.harm.prevent(action, context)
        decision.harm_assessment = HarmAssessmentSummary(
            [h.category for h in harm.potential_harms],
            max([h.probability for h in harm.potential_harms], default=0.0),
            harm.overall_risk,
            ["user"],
            all(h.reversible for h in harm.potential_harms) if harm.potential_harms else True,
        )
        if harm.overall_risk == "high":
            decision.decision = "escalate"
            conditions.append("harm_risk_high")

        if not self.containment.is_contained():
            decision.decision = "deny"
            conditions.append("containment_warning")

        rate_ok, rate_reason = self.rate.check_rate("goal_submissions")
        decision.rate_limit_check = rate_ok
        if not rate_ok:
            decision.decision = "deny"
            conditions.append(rate_reason)

        trust = self.trust.get_trust_level()
        decision.current_trust_level = trust.name.lower()
        decision.consent_required = self.consent.is_consent_required(decision.classification, trust)
        if decision.consent_required:
            rec = self.consent.request_consent(action, f"execute {action}", decision.risk_level.name, ["may impact system"], auto_response=context.get("auto_consent", True))
            decision.consent_obtained = rec.granted
            decision.consent_record_id = rec.record_id
            if not rec.granted:
                decision.decision = "deny"
                conditions.append("consent_denied")

        allowed = decision.decision in {"approve", "approve_with_conditions"} or (decision.decision == "escalate" and decision.consent_obtained)
        if decision.decision == "approve" and conditions:
            decision.decision = "approve_with_conditions"
        outcome = "allowed" if allowed else "denied" if decision.decision == "deny" else "escalated"
        self.audit.record(action, source_component, target, decision.decision_id, decision.classification.value, outcome, {"conditions": conditions})
        return InterceptResult(allowed, decision, conditions, payload)
