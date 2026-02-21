from __future__ import annotations
from dataclasses import dataclass
@dataclass
class RegressionResult: metric_name:str; baseline_value:float; current_value:float; change_percent:float; is_regression:bool; severity:str; recommendation:str
class RegressionDetector:
    def __init__(self,baseline_manager,metric_store,config): self.baseline_manager=baseline_manager;self.metric_store=metric_store;self.config=config;self.thresholds={}
    def set_regression_thresholds(self,thresholds): self.thresholds=thresholds
    def check_all_metrics(self,baseline):
        comp=self.baseline_manager.compare_to_baseline(baseline); out=[]
        for k,v in comp.items():
            b,c=v['baseline'],v['current'];ch=((c-b)/b*100 if b else 0);thr=self.thresholds.get(k,self.config.REGRESSION_THRESHOLD_PERCENT)
            reg=('latency' in k or 'error' in k) and ch>thr
            out.append(RegressionResult(k,b,c,ch,reg,'high' if reg else 'low','rollback' if reg else 'none'))
        return out
    def check_for_regressions(self,modification,duration_minutes=30): return [r for r in self.check_all_metrics(self.baseline_manager.get_current_baseline()) if r.is_regression]
    def monitor_after_modification(self,modification,duration_minutes=30): return self.check_for_regressions(modification,duration_minutes)
