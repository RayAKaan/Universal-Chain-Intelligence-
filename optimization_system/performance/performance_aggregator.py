from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from datetime import datetime
from optimization_system.utils.statistics_utils import mean, median, std_dev, percentile
@dataclass
class AggregatedMetric:
    metric_name:str; source_phase:str; window_start:datetime; window_end:datetime; count:int; mean:float; median:float; min:float; max:float; std_dev:float; p50:float; p95:float; p99:float; sum:float; trend:str
class PerformanceAggregator:
    def aggregate(self,metrics,window_seconds=3600):
        groups=defaultdict(list)
        for m in metrics: groups[(m.name,m.source_phase)].append(m)
        out=[]
        for (name,phase),vals in groups.items():
            nums=[v.value for v in vals];trend='stable' if len(nums)<2 else ('degrading' if nums[-1]>nums[0] else 'improving')
            out.append(AggregatedMetric(name,phase,min(v.timestamp for v in vals),max(v.timestamp for v in vals),len(nums),mean(nums),median(nums),min(nums),max(nums),std_dev(nums),percentile(nums,50),percentile(nums,95),percentile(nums,99),sum(nums),trend))
        return out
    def aggregate_by_phase(self,metrics):
        out=defaultdict(list)
        for a in self.aggregate(metrics): out[a.source_phase].append(a)
        return dict(out)
    def aggregate_by_component(self,metrics):
        out=defaultdict(list)
        for m in metrics: out[m.source_component].append(m)
        return {k:self.aggregate(v) for k,v in out.items()}
    def aggregate_by_type(self,metrics):
        out=defaultdict(list)
        for m in metrics: out[m.metric_type.value].append(m)
        return {k:self.aggregate(v) for k,v in out.items()}
    def get_current_summary(self): return {'status':'ok'}
    def compare_windows(self,a,b):
        bm={x.metric_name:x for x in b};return {x.metric_name:{'delta':x.mean-bm[x.metric_name].mean,'percent_change':((x.mean-bm[x.metric_name].mean)/bm[x.metric_name].mean*100 if bm[x.metric_name].mean else 0)} for x in a if x.metric_name in bm}
