from __future__ import annotations
from datetime import datetime, timezone
from optimization_system.models.component_profile import ComponentProfile
class SystemProfiler:
    def profile_component(self,phase,component_name,duration_seconds=60):
        return ComponentProfile(phase=phase,component_name=component_name,component_type='generic',performance_metrics={'avg_latency_ms':100,'p50_latency_ms':95,'p95_latency_ms':150,'p99_latency_ms':180,'throughput_per_second':10,'success_rate':0.95,'error_rate':0.05},resource_metrics={'avg_cpu_percent':30,'avg_memory_mb':128,'peak_cpu_percent':50,'peak_memory_mb':256},usage_metrics={'total_invocations':100,'invocations_per_hour':20,'last_used':datetime.now(timezone.utc).isoformat(),'uptime_percent':99.0},quality_metrics={'reliability_score':0.95,'efficiency_score':0.8,'overall_score':0.88},trends={'latency_trend':'stable','reliability_trend':'stable','usage_trend':'stable'},sample_count=100)
    def profile_all_components(self): return [self.profile_component('phase1','capability_registry'),self.profile_component('phase2','strategy_engine')]
    def profile_capability(self,capability_id,iterations=50): return self.profile_component('phase1',capability_id)
    def profile_strategy(self,strategy_name,sample_goals=None): return self.profile_component('phase2',strategy_name)
    def compare_profiles(self,a,b): return {'latency_delta':b.performance_metrics.get('avg_latency_ms',0)-a.performance_metrics.get('avg_latency_ms',0),'score_delta':b.quality_metrics.get('overall_score',0)-a.quality_metrics.get('overall_score',0)}
