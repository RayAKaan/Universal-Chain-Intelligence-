from __future__ import annotations
from optimization_system.utils.statistics_utils import correlation
class PatternExtractor:
    def extract_performance_patterns(self,metrics): return [{'type':'high_latency_cluster','count':len([m for m in metrics if 'latency' in m.name and m.value>300])}]
    def extract_failure_patterns(self,execution_history): return [{'type':'failure_sequence','count':len([x for x in execution_history if not x.get('success',True)])}]
    def extract_success_patterns(self,execution_history): return [{'type':'success_sequence','count':len([x for x in execution_history if x.get('success',True)])}]
    def extract_correlations(self,metrics):
        vals=[m.value for m in metrics]
        return [{'metric_a':'index','metric_b':'value','correlation':correlation(list(range(len(vals))),vals)}] if vals else []
