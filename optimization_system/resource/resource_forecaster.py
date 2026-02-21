from __future__ import annotations
from datetime import datetime, timedelta, timezone
from optimization_system.utils.time_series_utils import forecast_next
class ResourceForecaster:
    def __init__(self,metric_store): self.store=metric_store
    def forecast_usage(self,metric_name,hours_ahead=24):
        vals=[m.value for m in self.store.get_history(metric_name,24)] or [50.0]
        return forecast_next(vals,hours_ahead)
    def forecast_capacity_exhaustion(self,resource):
        for i,v in enumerate(self.forecast_usage(f'system_{resource}_usage_percent',24)):
            if v>=95:return datetime.now(timezone.utc)+timedelta(hours=i+1)
        return None
