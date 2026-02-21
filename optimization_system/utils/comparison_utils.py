from __future__ import annotations

def is_improvement(before,after,metric_type):
    m=metric_type.lower();return after<before if any(x in m for x in ['latency','error','resource','time']) else after>before
def improvement_percent(before,after,metric_type):
    if before==0:return 0.0
    return abs(after-before)/abs(before)*100.0
def compare_metrics(before,after):
    keys=set(before)|set(after);out={}
    for k in keys:
        b,a=before.get(k,0.0),after.get(k,0.0)
        out[k]={'before':b,'after':a,'change':a-b,'change_percent':((a-b)/b*100.0 if b else 0.0),'improved':is_improvement(b,a,k)}
    return out
def compare_profiles(a,b): return compare_metrics(a.performance_metrics,b.performance_metrics)
