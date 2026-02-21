from __future__ import annotations
from optimization_system.utils.statistics_utils import exponential_smoothing, linear_regression

def moving_average(values,window=5): return [sum(values[max(0,i-window+1):i+1])/len(values[max(0,i-window+1):i+1]) for i in range(len(values))] if values else []
def exponential_moving_average(values,alpha=0.3): return exponential_smoothing(values,alpha)
def detect_trend(values):
    if len(values)<2:return 'stable'
    slope,_=linear_regression(list(range(len(values))),values)
    return 'increasing' if slope>0.01 else 'decreasing' if slope<-0.01 else 'stable'
def detect_change_point(values):
    if len(values)<3:return -1
    m=sum(values)/len(values);best=0;idx=-1
    for i in range(len(values)):
        s=abs(sum(values[:i+1])-(i+1)*m)
        if s>best:best=s;idx=i
    return idx
def forecast_next(values,periods=1): return [exponential_smoothing(values)[-1] if values else 0.0 for _ in range(periods)]
def seasonal_decompose(values,period): return {'trend':moving_average(values,period),'seasonal':[0]*len(values),'residual':[0]*len(values)}
