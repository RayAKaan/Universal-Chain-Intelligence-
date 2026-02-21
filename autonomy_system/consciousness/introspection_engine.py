from __future__ import annotations
class IntrospectionEngine:
    def __init__(self,system_state=None): self.system_state=system_state
    def introspect(self):
        s=self.system_state.snapshot() if self.system_state else {}
        return {'capability_inventory':s.get('counters',{}).get('capabilities',0),'performance_profile':{},'resource_utilization':{},'learning_progress':{},'improvement_history':{},'failure_patterns':{},'strength_areas':self.get_strengths(),'weakness_areas':self.get_weaknesses()}
    def get_strengths(self): return ['deterministic execution','modular planning']
    def get_weaknesses(self): return ['limited external integrations by default']
    def get_recent_learnings(self): return ['fast_processor has better latency than slow_processor']
