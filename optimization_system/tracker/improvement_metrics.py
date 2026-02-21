from __future__ import annotations
from datetime import datetime, timezone
class ImprovementMetrics:
    def __init__(self,tracker): self.tracker=tracker
    def calculate_improvement_velocity(self):
        items=self.tracker.get_all_improvements()
        if not items:return 0.0
        days=max(1,(datetime.now(timezone.utc)-min(i.created_at for i in items)).days)
        return len(items)/days
    def calculate_success_rate(self):
        items=self.tracker.get_all_improvements();
        if not items:return 0.0
        return len([i for i in items if i.status.value in {'APPLIED','VERIFIED'}])/len(items)
    def calculate_cumulative_impact(self): return self.tracker.get_improvement_impact()
    def calculate_roi(self):
        items=self.tracker.get_all_improvements()
        return sum(sum(i.improvement_percent.values()) for i in items)/max(1,len(items))
