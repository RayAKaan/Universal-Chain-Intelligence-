from __future__ import annotations
class HotspotFinder:
    def find_hotspots(self,metrics,threshold_percentile=95):
        vals=sorted([m.value for m in metrics])
        if not vals:return []
        thr=vals[max(0,int(len(vals)*threshold_percentile/100)-1)]
        return [{'component':m.source_component,'metric':m.name,'value':m.value} for m in metrics if m.value>=thr]
    def find_cold_spots(self,metrics):
        if not metrics:return []
        avg=sum(m.value for m in metrics)/len(metrics)
        return [{'component':m.source_component,'metric':m.name,'value':m.value} for m in metrics if m.value<0.5*avg]
