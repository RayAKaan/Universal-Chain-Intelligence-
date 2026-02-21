from __future__ import annotations
from optimization_system.utils.statistics_utils import mean
class PerformanceAnalyzer:
    def __init__(self,metric_store,phase1_bridge=None,phase2_bridge=None): self.store=metric_store;self.p1=phase1_bridge;self.p2=phase2_bridge
    def analyze_system_health(self):
        m=self.store.query(limit=200);score=max(0.0,min(1.0,1.0-mean([x.value for x in m if 'error' in x.name])/100 if m else 0.8))
        return {'overall_health':'healthy' if score>0.75 else 'degraded','overall_score':score,'phase_health':{'phase0':'healthy','phase1':'healthy','phase2':'healthy','phase3':'healthy'},'critical_issues':[],'warnings':[],'top_performers':[],'worst_performers':[],'recommendations':['continue monitoring']}
    def analyze_capability_performance(self):
        d=self.p1.get_all_capability_performances() if self.p1 else {}
        ranked=sorted(d.items(),key=lambda x:(x[1].get('reliability',0),-x[1].get('latency_ms',9999)),reverse=True)
        return {'ranked':ranked,'underperformers':[k for k,v in d.items() if v.get('reliability',1)<0.9 or v.get('latency_ms',0)>300]}
    def analyze_strategy_effectiveness(self): return {'strategies':self.p2.get_strategy_performance() if self.p2 else {}}
    def analyze_resource_efficiency(self):
        cpu=self.store.get_latest('system_cpu_usage_percent'); mem=self.store.get_latest('system_memory_usage_percent')
        return {'cpu':cpu.value if cpu else 0,'memory':mem.value if mem else 0,'recommendations':['reallocate resources if high']}
    def analyze_trends(self,metric_name,window_hours=24):
        h=self.store.get_history(metric_name,window_hours);vals=[x.value for x in h];trend='stable' if len(vals)<2 else ('degrading' if vals[-1]>vals[0] else 'improving')
        return {'metric':metric_name,'trend':trend,'slope':0.0,'change_percent':((vals[-1]-vals[0])/vals[0]*100 if len(vals)>1 and vals[0] else 0),'forecast_next_hour':vals[-1] if vals else 0,'anomalies':[]}
    def get_performance_score(self,phase=None,component=None):
        ms=self.store.query(source_phase=phase,source_component=component,limit=200)
        if not ms:return 0.8
        return max(0.0,min(1.0,1.0-mean([m.value for m in ms if 'latency' in m.name])/1000.0))
