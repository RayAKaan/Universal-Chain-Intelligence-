from __future__ import annotations
from datetime import datetime, timezone
class RollbackEngine:
    def rollback(self,modification):
        if not modification.rollback_available: return False
        modification.rolled_back=True; modification.rolled_back_at=datetime.now(timezone.utc); modification.applied=False; return True
    def rollback_batch(self,modifications): return all(self.rollback(m) for m in reversed(modifications))
    def is_rollback_available(self,modification): return modification.rollback_available
    def get_rollback_chain(self,modification_id): return []
