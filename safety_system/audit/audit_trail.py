from datetime import datetime

from safety_system.audit.audit_integrity import calculate_entry_hash, detect_tampering
from safety_system.models.audit_entry import AuditEntry


class AuditTrail:
    def __init__(self, audit_store, config):
        self.store = audit_store

    def record(self, action: str, actor: str, target: str, safety_decision_id: str, classification: str, outcome: str, details: dict = None) -> AuditEntry:
        prev = self.store.all()[-1] if self.store.all() else None
        seq = 1 if prev is None else prev.sequence_number + 1
        prev_hash = "GENESIS" if prev is None else prev.entry_hash
        entry = AuditEntry(seq, action, actor, target, safety_decision_id, classification, outcome, prev_hash, "", details or {})
        entry.entry_hash = calculate_entry_hash(entry)
        self.store.append(entry)
        return entry

    def verify_integrity(self) -> tuple[bool, list[str]]:
        issues = detect_tampering(self.store.all())
        return len(issues) == 0, issues

    def get_entries(self, start: datetime = None, end: datetime = None, limit: int = 1000):
        entries = self.store.all()
        if start:
            entries = [e for e in entries if e.timestamp >= start]
        if end:
            entries = [e for e in entries if e.timestamp <= end]
        return entries[-limit:]

    def search(self, query: str):
        q = query.lower()
        return [e for e in self.store.all() if q in str(e.details).lower() or q in e.action.lower()]

    def get_entry(self, entry_id: str):
        return self.store.by_id(entry_id)

    def get_latest(self, limit: int = 10):
        return self.store.all()[-limit:]

    def count(self) -> int:
        return len(self.store.all())

    def get_stats(self) -> dict:
        return {"entries": self.count(), "latest_seq": self.store.all()[-1].sequence_number if self.store.all() else 0}
