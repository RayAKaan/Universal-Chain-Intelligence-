from datetime import datetime, timedelta, timezone

from safety_system.models.consent_record import ConsentRecord, ConsentType
from safety_system.models.safety_decision import ActionClassification
from safety_system.models.trust_level import TrustTier


class ConsentManager:
    def __init__(self, consent_store, approval_workflow, config):
        self.store = consent_store
        self.workflow = approval_workflow
        self.config = config

    def request_consent(self, action: str, description: str, risk_level: str, consequences: list[str], auto_response: bool = True, granted_by: str = "human") -> ConsentRecord:
        _msg = self.workflow.format_request(action, description, risk_level, consequences)
        granted = bool(auto_response)
        rec = ConsentRecord(
            action=action,
            description=description,
            consent_type=ConsentType.ONE_TIME,
            granted=granted,
            granted_by=granted_by,
            valid_until=datetime.now(timezone.utc) + timedelta(seconds=self.config.BLANKET_CONSENT_DURATION_SECONDS),
            metadata={"request": _msg},
        )
        self.store.add(rec)
        return rec

    def has_consent(self, action: str) -> bool:
        now = datetime.now(timezone.utc)
        return any(r.action == action and r.granted and not r.revoked and (r.valid_until is None or r.valid_until > now) for r in self.store.all())

    def revoke_consent(self, record_id: str) -> None:
        rec = self.store.get(record_id)
        if rec:
            rec.revoked = True
            rec.revoked_at = datetime.now(timezone.utc)

    def revoke_all_consent(self) -> None:
        for rec in self.store.all():
            rec.revoked = True
            rec.revoked_at = datetime.now(timezone.utc)

    def get_consent_history(self):
        return self.store.all()

    def is_consent_required(self, classification: ActionClassification, trust_level: TrustTier) -> bool:
        if classification == ActionClassification.FORBIDDEN:
            return False
        if classification == ActionClassification.SAFE:
            return False
        if classification == ActionClassification.CAUTION:
            return trust_level == TrustTier.PROBATIONARY
        if classification == ActionClassification.RISKY:
            return trust_level < TrustTier.TRUSTED
        return classification == ActionClassification.DANGEROUS
