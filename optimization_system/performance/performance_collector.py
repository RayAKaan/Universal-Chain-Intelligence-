from __future__ import annotations
from datetime import datetime, timezone
try:
    import psutil
except Exception:
    psutil=None
from optimization_system.models.metric import Metric, MetricType
class PerformanceCollector:
    def __init__(self,phase0_bridge,phase1_bridge,phase2_bridge,phase3_bridge,metric_store,config): self.p0=phase0_bridge;self.p1=phase1_bridge;self.p2=phase2_bridge;self.p3=phase3_bridge;self.store=metric_store;self.config=config
    def _m(self,name,t,p,c,v,u=''):
        now=datetime.now(timezone.utc)
        return Metric(name=name,metric_type=t,source_phase=p,source_component=c,value=float(v),unit=u,window_start=now,window_end=now)
    def collect_phase0_metrics(self):
        d=self.p0.get_execution_metrics();return [self._m('execution_latency_ms',MetricType.LATENCY,'phase0','execution_engine',d.get('avg_latency_ms',0),'ms'),self._m('execution_success_rate',MetricType.SUCCESS_RATE,'phase0','execution_engine',d.get('success_rate',0)),self._m('queue_depth',MetricType.QUEUE_DEPTH,'phase0','scheduler',d.get('queue_depth',0))]
    def collect_phase1_metrics(self):
        d=self.p1.get_capability_metrics();return [self._m('capability_count',MetricType.CAPABILITY_COUNT,'phase1','registry',d.get('total_capabilities',0)),self._m('healthy_capability_count',MetricType.HEALTHY_CAPABILITY_COUNT,'phase1','registry',d.get('healthy_capabilities',0)),self._m('capability_latency_ms',MetricType.LATENCY,'phase1','capabilities',d.get('average_latency_ms',0),'ms')]
    def collect_phase2_metrics(self):
        d=self.p2.get_planning_metrics();return [self._m('planning_duration_ms',MetricType.PLANNING_TIME,'phase2','planning_engine',d.get('avg_planning_duration_ms',0),'ms'),self._m('plan_success_rate',MetricType.SUCCESS_RATE,'phase2','planning_engine',d.get('execution_success_rate',0)),self._m('parallel_efficiency',MetricType.PARALLEL_EFFICIENCY,'phase2','strategy_engine',d.get('parallel_efficiency',0))]
    def collect_phase3_metrics(self):
        d=self.p3.get_construction_metrics();return [self._m('build_success_rate',MetricType.BUILD_SUCCESS_RATE,'phase3','construction_manager',d.get('build_success_rate',0)),self._m('sandbox_success_rate',MetricType.SANDBOX_SUCCESS_RATE,'phase3','sandbox',d.get('sandbox_success_rate',0)),self._m('artifact_count',MetricType.CUSTOM,'phase3','artifact_manager',d.get('artifact_count',0))]
    def collect_system_metrics(self):
        cpu=psutil.cpu_percent() if psutil else 50.0; mem=psutil.virtual_memory().percent if psutil else 50.0
        return [self._m('system_cpu_usage_percent',MetricType.RESOURCE_USAGE_CPU,'system','host',cpu,'%'),self._m('system_memory_usage_percent',MetricType.RESOURCE_USAGE_MEMORY,'system','host',mem,'%')]
    def collect_all(self):
        out=self.collect_phase0_metrics()+self.collect_phase1_metrics()+self.collect_phase2_metrics()+self.collect_phase3_metrics()+self.collect_system_metrics();self.store.store_batch(out);return out
    def start_continuous_collection(self,interval_seconds=60): pass
    def stop_continuous_collection(self): pass
