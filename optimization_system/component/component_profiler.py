from __future__ import annotations
from optimization_system.performance.system_profiler import SystemProfiler
class ComponentProfiler:
    def __init__(self,profiler=None): self.profiler=profiler or SystemProfiler()
    def profile(self,phase,component,sample_count=100): return self.profiler.profile_component(phase,component)
    def compare(self,a,b): return self.profiler.compare_profiles(a,b)
    def identify_weaknesses(self,p):
        out=[]
        if p.performance_metrics.get('avg_latency_ms',0)>300: out.append('high_latency')
        if p.performance_metrics.get('success_rate',1)<0.9: out.append('low_reliability')
        return out
    def score_component(self,p): return p.quality_metrics.get('overall_score',0.5)
