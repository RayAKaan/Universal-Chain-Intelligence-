from __future__ import annotations
from collections import defaultdict
class TelemetryAggregator:
    def aggregate(self,points,window_seconds=60):
        g=defaultdict(list)
        for p in points:g[(p.category,p.name)].append(p.value)
        return [{'category':k[0],'name':k[1],'mean':sum(v)/len(v),'count':len(v)} for k,v in g.items()]
    def get_dashboard_data(self): return {'status':'ok'}
