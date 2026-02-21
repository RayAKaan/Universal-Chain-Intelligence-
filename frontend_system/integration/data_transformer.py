
from datetime import datetime, timezone


def _iso(v):
    if isinstance(v, datetime):
        return v.isoformat()
    return v


def _ago(ts):
    try:
        if isinstance(ts,str):
            dt=datetime.fromisoformat(ts.replace('Z','+00:00'))
        else:
            dt=ts
        s=(datetime.now(timezone.utc)-dt).total_seconds()
        if s<60:return f"{int(s)}s ago"
        if s<3600:return f"{int(s//60)}m ago"
        if s<86400:return f"{int(s//3600)}h ago"
        return f"{int(s//86400)}d ago"
    except Exception:
        return 'unknown'

class DataTransformer:
    def transform_capability(self,c):
        d=dict(c); d['updated_at']=_iso(d.get('updated_at')); d['time_ago']=_ago(d.get('updated_at')); return d
    def transform_goal(self,g):
        d=dict(g); d['submitted_at']=_iso(d.get('submitted_at')); d['time_ago']=_ago(d.get('submitted_at')); return d
    def transform_plan(self,p):
        return dict(p)
    def transform_improvement(self,i):
        return dict(i)
    def transform_safety_decision(self,d):
        return dict(d)
    def transform_metric(self,m):
        return dict(m)
    def transform_timeline_event(self,e):
        d=dict(e); d['time_ago']=_ago(d.get('timestamp')); return d
