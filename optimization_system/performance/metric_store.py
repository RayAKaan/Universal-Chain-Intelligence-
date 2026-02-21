from __future__ import annotations
from datetime import datetime, timedelta, timezone
from optimization_system.models.metric import Metric, MetricType
from optimization_system.persistence.serialization import serialize, deserialize
class MetricStore:
    def __init__(self,db): self.db=db
    def store(self,metric):
        self.db.execute('INSERT OR REPLACE INTO metrics(metric_id,name,metric_type,source_phase,source_component,value,unit,timestamp,data) VALUES(?,?,?,?,?,?,?,?,?)',(metric.metric_id,metric.name,metric.metric_type.value,metric.source_phase,metric.source_component,metric.value,metric.unit,metric.timestamp.isoformat(),serialize(metric)))
    def store_batch(self,metrics):
        for m in metrics:self.store(m)
    def query(self,metric_type=None,source_phase=None,source_component=None,start_time=None,end_time=None,limit=1000):
        q='SELECT data FROM metrics WHERE 1=1';p=[]
        if metric_type:q+=' AND metric_type=?';p.append(metric_type.value if hasattr(metric_type,'value') else metric_type)
        if source_phase:q+=' AND source_phase=?';p.append(source_phase)
        if source_component:q+=' AND source_component=?';p.append(source_component)
        if start_time:q+=' AND timestamp>=?';p.append(start_time.isoformat())
        if end_time:q+=' AND timestamp<=?';p.append(end_time.isoformat())
        q+=' ORDER BY timestamp DESC LIMIT ?';p.append(limit)
        rows=self.db.query(q,tuple(p));out=[]
        for r in rows:
            d=deserialize(r['data']);d['metric_type']=MetricType(d.get('metric_type','CUSTOM'))
            for k in ['timestamp','window_start','window_end']:
                if d.get(k):d[k]=datetime.fromisoformat(d[k])
            out.append(Metric(**d))
        return out
    def get_latest(self,metric_name,source_phase=None):
        for m in self.query(source_phase=source_phase,limit=1000):
            if m.name==metric_name:return m
        return None
    def get_history(self,metric_name,hours=24):
        st=datetime.now(timezone.utc)-timedelta(hours=hours)
        return [m for m in self.query(start_time=st,limit=10000) if m.name==metric_name]
    def get_aggregated(self,metric_name,window_seconds=3600,hours=24):
        from optimization_system.performance.performance_aggregator import PerformanceAggregator
        return PerformanceAggregator().aggregate(self.get_history(metric_name,hours),window_seconds)
    def purge_old(self,days=30):
        cutoff=(datetime.now(timezone.utc)-timedelta(days=days)).isoformat();cur=self.db.execute('DELETE FROM metrics WHERE timestamp<?',(cutoff,));return cur.rowcount
    def get_stats(self): return {'total_metrics':self.db.query('SELECT COUNT(*) c FROM metrics')[0]['c']}
