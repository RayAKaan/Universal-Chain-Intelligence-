from __future__ import annotations
class CapabilityRanker:
    def __init__(self,phase1_bridge,config): self.p1=phase1_bridge;self.config=config
    def _score(self,p):
        w=self.config.CAPABILITY_SCORE_WEIGHTS
        rel=p.get('reliability',0.0);lat=1.0/(1.0+p.get('latency_ms',100)/100.0);use=min(1.0,p.get('usage',1)/10.0);health=1.0 if p.get('reliability',0)>=0.9 else 0.5
        return rel*w['reliability']+lat*w['latency']+use*w['usage']+health*w['health']
    def rank_all(self):
        perf=self.p1.get_all_capability_performances();return sorted([(cid,self._score(v)) for cid,v in perf.items()],key=lambda x:x[1],reverse=True)
    def rank_by_value(self):
        perf=self.p1.get_all_capability_performances();return sorted([(cid,self._score(v)*v.get('usage',1)) for cid,v in perf.items()],key=lambda x:x[1],reverse=True)
    def identify_underperformers(self,threshold=0.3): return [cid for cid,s in self.rank_all() if s<threshold]
    def identify_redundant(self):
        perf=self.p1.get_all_capability_performances();groups={}
        for cid,v in perf.items(): groups.setdefault(v.get('name','generic').split('_')[-1],[]).append(cid)
        return [g for g in groups.values() if len(g)>1]
