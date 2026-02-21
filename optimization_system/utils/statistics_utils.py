from __future__ import annotations
import math, statistics

def mean(v): return statistics.fmean(v) if v else 0.0
def median(v): return statistics.median(v) if v else 0.0
def variance(v): return statistics.variance(v) if len(v)>1 else 0.0
def std_dev(v): return math.sqrt(variance(v))
def percentile(v,p):
    if not v:return 0.0
    s=sorted(v);k=(len(s)-1)*(p/100.0);f=math.floor(k);c=math.ceil(k)
    return s[int(k)] if f==c else s[f]*(c-k)+s[c]*(k-f)
def iqr(v): return percentile(v,75)-percentile(v,25)
def linear_regression(x,y):
    n=min(len(x),len(y));
    if n<2:return 0.0,0.0
    x,y=x[:n],y[:n];mx,my=mean(x),mean(y)
    den=sum((a-mx)**2 for a in x)
    if den==0:return 0.0,my
    slope=sum((x[i]-mx)*(y[i]-my) for i in range(n))/den
    return slope,my-slope*mx
def correlation(x,y):
    n=min(len(x),len(y))
    if n<2:return 0.0
    x,y=x[:n],y[:n];mx,my=mean(x),mean(y)
    num=sum((x[i]-mx)*(y[i]-my) for i in range(n));den=math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
    return num/den if den else 0.0
def _cdf(z): return (1+math.erf(z/math.sqrt(2)))/2
def t_test(a,b):
    if len(a)<2 or len(b)<2:return 1.0
    ma,mb=mean(a),mean(b);va,vb=variance(a),variance(b);se=math.sqrt(va/len(a)+vb/len(b))
    if se==0:return 1.0
    t=abs(ma-mb)/se
    return max(0.0,min(1.0,2*(1-_cdf(t))))
def z_score(v,m,s): return 0.0 if s==0 else (v-m)/s
def exponential_smoothing(values,alpha=0.3):
    if not values:return []
    out=[values[0]]
    for v in values[1:]:out.append(alpha*v+(1-alpha)*out[-1])
    return out
def detect_outliers_zscore(values,threshold=2.0):
    m=mean(values);s=std_dev(values)
    return [i for i,v in enumerate(values) if abs(z_score(v,m,s))>threshold]
def detect_outliers_iqr(values):
    q1,q3=percentile(values,25),percentile(values,75);r=q3-q1;lo,hi=q1-1.5*r,q3+1.5*r
    return [i for i,v in enumerate(values) if v<lo or v>hi]
def normalize(values):
    if not values:return []
    lo,hi=min(values),max(values)
    return [1.0 for _ in values] if lo==hi else [(v-lo)/(hi-lo) for v in values]
