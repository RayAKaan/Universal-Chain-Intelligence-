from __future__ import annotations
from optimization_system.utils.statistics_utils import linear_regression, detect_outliers_zscore, exponential_smoothing
class TrendDetector:
    def detect_trend(self,values,timestamps):
        if len(values)<2:return 'stable'
        slope,_=linear_regression(list(range(len(values))),values)
        return 'improving' if slope<0 else 'degrading' if slope>0 else 'stable'
    def detect_anomaly(self,values): return detect_outliers_zscore(values,2.0)
    def detect_change_point(self,values):
        if len(values)<3:return -1
        m=sum(values)/len(values);best=0;idx=-1
        for i in range(len(values)):
            s=abs(sum(values[:i+1])-(i+1)*m)
            if s>best: best=s; idx=i
        return idx
    def forecast(self,values,periods=10):
        if not values:return [0.0]*periods
        sm=exponential_smoothing(values)
        return [sm[-1] for _ in range(periods)]
    def detect_seasonality(self,values):
        if len(values)<4:return {'period':None,'amplitude':0.0}
        return {'period':max(2,len(values)//4),'amplitude':(max(values)-min(values))/2}
