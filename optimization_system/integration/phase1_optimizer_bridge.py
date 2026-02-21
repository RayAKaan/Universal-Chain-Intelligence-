from __future__ import annotations
class Phase1OptimizerBridge:
    def __init__(self,capability_registry,query_engine,benchmark_engine,lifecycle_manager,event_bus): self.registry=capability_registry;self.query=query_engine;self.bench=benchmark_engine;self.lifecycle=lifecycle_manager;self.event_bus=event_bus
    def get_capability_metrics(self):
        caps=self.registry.get_all();healthy=sum(1 for c in caps if (c.metadata or {}).get('reliability',1.0)>=0.9)
        avg=sum((c.metadata or {}).get('latency_ms',100) for c in caps)/len(caps) if caps else 0
        return {'total_capabilities':len(caps),'active_capabilities':len(caps),'healthy_capabilities':healthy,'average_latency_ms':avg}
    def get_capability_performance(self,capability_id):
        c=next((c for c in self.registry.get_all() if c.capability_id==capability_id),None); md=c.metadata if c else {}
        return {'latency_ms':md.get('latency_ms',100),'reliability':md.get('reliability',0.95),'days_since_used':md.get('days_since_used',0),'usage':md.get('usage',1)}
    def get_all_capability_performances(self):
        return {c.capability_id:{'name':c.name,'latency_ms':(c.metadata or {}).get('latency_ms',100),'reliability':(c.metadata or {}).get('reliability',0.95),'days_since_used':(c.metadata or {}).get('days_since_used',0),'usage':(c.metadata or {}).get('usage',1)} for c in self.registry.get_all()}
    def replace_capability(self,old_id,new_id): return True
    def deactivate_capability(self,capability_id): return True
    def activate_capability(self,capability_id): return True
    def benchmark_capability(self,capability_id): return {'score':0.8}
    def get_capability_usage_stats(self): return {c.capability_id:(c.metadata or {}).get('usage',1) for c in self.registry.get_all()}
