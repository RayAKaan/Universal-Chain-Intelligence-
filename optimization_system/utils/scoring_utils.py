from __future__ import annotations

def normalize_score(value,min_val,max_val): return 1.0 if max_val==min_val else max(0.0,min(1.0,(value-min_val)/(max_val-min_val)))
def composite_score(metrics,weights):
    total=sum(weights.values()) or 1.0
    return sum(metrics.get(k,0.0)*w for k,w in weights.items())/total
def rank_items(items,score_func): return sorted(items,key=score_func,reverse=True)
