from __future__ import annotations
import json
from optimization_system.models.baseline import Baseline
class BaselineManager:
    def __init__(self,metric_store,db): self.store=metric_store;self.db=db;self.current=None
    def _metrics(self):
        names=['execution_avg_latency_ms','execution_success_rate','planning_avg_duration_ms','resolution_avg_duration_ms','construction_success_rate','capability_count','active_capability_count','healthy_capability_count','strategy_count','avg_plan_steps','avg_parallel_efficiency','system_cpu_usage_percent','system_memory_usage_percent']
        out={}
        for n in names:
            m=self.store.get_latest(n) or self.store.get_latest(n.replace('execution_avg_latency_ms','execution_latency_ms').replace('planning_avg_duration_ms','planning_duration_ms'))
            out[n]=m.value if m else 0.0
        return out
    def capture_baseline(self,name=None):
        b=Baseline(name=name or 'baseline',metrics=self._metrics()); self.current=b
        self.db.execute('INSERT OR REPLACE INTO baselines(baseline_id,name,data,timestamp) VALUES(?,?,?,?)',(b.baseline_id,b.name,json.dumps({'metrics':b.metrics}),b.timestamp.isoformat()))
        return b
    def get_current_baseline(self): return self.current or self.capture_baseline('auto')
    def get_baseline(self,baseline_id):
        r=self.db.query('SELECT * FROM baselines WHERE baseline_id=?',(baseline_id,))
        if not r:return None
        d=json.loads(r[0]['data']); return Baseline(name=r[0]['name'],metrics=d.get('metrics',{}),baseline_id=r[0]['baseline_id'])
    def get_all_baselines(self): return [self.get_baseline(r['baseline_id']) for r in self.db.query('SELECT baseline_id FROM baselines')]
    def compare_to_baseline(self,baseline):
        cur=self._metrics(); return {k:{'baseline':baseline.metrics.get(k,0),'current':cur.get(k,0),'delta':cur.get(k,0)-baseline.metrics.get(k,0)} for k in set(cur)|set(baseline.metrics)}
    def update_baseline(self,baseline_id):
        b=self.get_baseline(baseline_id)
        if b: b.metrics=self._metrics()
        return b
