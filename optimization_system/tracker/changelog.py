from __future__ import annotations
from datetime import datetime, timedelta, timezone
class Changelog:
    def __init__(self,history): self.history=history
    def generate_changelog(self,since=None):
        events=self.history.get_full_changelog()
        if since: events=[e for e in events if e.get('timestamp','')>=since.isoformat()]
        return '\n'.join(f"- {e.get('timestamp')} | {e.get('event_type')} | {e.get('improvement_id')}" for e in events) or 'No changes.'
    def generate_summary(self,period_days=7): return self.generate_changelog(datetime.now(timezone.utc)-timedelta(days=period_days))
