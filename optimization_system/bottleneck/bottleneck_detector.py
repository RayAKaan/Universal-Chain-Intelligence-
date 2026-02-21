from __future__ import annotations
from optimization_system.models.bottleneck import Bottleneck, BottleneckType, Severity
from optimization_system.bottleneck.bottleneck_analyzer import BottleneckAnalyzer
class BottleneckDetector:
    def __init__(self,performance_analyzer,metric_store,config): self.pa=performance_analyzer;self.store=metric_store;self.config=config;self.active={};self.analyzer=BottleneckAnalyzer()
    def _mk(self,*args,**kwargs):
        b=Bottleneck(*args,**kwargs);b.impact=self.analyzer.analyze_impact(b);b.suggested_actions=self.analyzer.suggest_actions(b);self.active[b.bottleneck_id]=b;return b
    def detect_slow_capabilities(self):
        out=[];perf=self.pa.analyze_capability_performance().get('ranked',[]);lats=[v.get('latency_ms',0) for _,v in perf if isinstance(v,dict)];avg=sum(lats)/len(lats) if lats else 0
        for cid,v in perf:
            lat=v.get('latency_ms',0)
            if avg and lat>self.config.LATENCY_BOTTLENECK_MULTIPLIER*avg: out.append(self._mk(BottleneckType.SLOW_CAPABILITY,Severity.HIGH,'phase1',cid,'Slow capability','latency_ms',lat,avg,(lat-avg)/avg*100.0))
        return out
    def detect_high_failure_rates(self):
        out=[]
        for cid,v in self.pa.analyze_capability_performance().get('ranked',[]):
            err=1.0-v.get('reliability',1.0)
            if err>self.config.FAILURE_RATE_THRESHOLD: out.append(self._mk(BottleneckType.HIGH_FAILURE_RATE,Severity.HIGH,'phase1',cid,'High failure rate','error_rate',err,self.config.FAILURE_RATE_THRESHOLD,(err-self.config.FAILURE_RATE_THRESHOLD)/self.config.FAILURE_RATE_THRESHOLD*100))
        return out
    def detect_resource_bottlenecks(self):
        out=[]
        for name in ['system_cpu_usage_percent','system_memory_usage_percent']:
            m=self.store.get_latest(name)
            if m and m.value/100.0>self.config.RESOURCE_USAGE_THRESHOLD: out.append(self._mk(BottleneckType.RESOURCE_CONTENTION,Severity.MEDIUM,'system','host',f'{name} high',name,m.value,self.config.RESOURCE_USAGE_THRESHOLD*100,(m.value-self.config.RESOURCE_USAGE_THRESHOLD*100)/(self.config.RESOURCE_USAGE_THRESHOLD*100)*100))
        return out
    def detect_planning_bottlenecks(self): return []
    def detect_construction_bottlenecks(self): return []
    def detect_queue_bottlenecks(self): return []
    def detect_stale_capabilities(self):
        out=[];perf=self.pa.p1.get_all_capability_performances() if self.pa.p1 else {}
        for cid,v in perf.items():
            age=v.get('days_since_used',0)
            if age>self.config.STALE_CAPABILITY_DAYS: out.append(self._mk(BottleneckType.STALE_CAPABILITIES,Severity.LOW,'phase1',cid,'Stale capability','days_since_used',age,self.config.STALE_CAPABILITY_DAYS,(age-self.config.STALE_CAPABILITY_DAYS)/self.config.STALE_CAPABILITY_DAYS*100.0))
        return out
    def detect_all(self):
        bs=self.detect_slow_capabilities()+self.detect_high_failure_rates()+self.detect_resource_bottlenecks()+self.detect_planning_bottlenecks()+self.detect_construction_bottlenecks()+self.detect_queue_bottlenecks()+self.detect_stale_capabilities()
        return sorted({(b.bottleneck_type,b.component):b for b in bs}.values(),key=lambda x:x.severity.value)
    def get_active_bottlenecks(self): return list(self.active.values())
    def get_bottleneck_history(self,hours=24): return list(self.active.values())
    def resolve_bottleneck(self,bottleneck_id,resolution):
        if bottleneck_id in self.active: self.active[bottleneck_id].status='resolved'; self.active[bottleneck_id].resolution=resolution
