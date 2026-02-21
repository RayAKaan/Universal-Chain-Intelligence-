from __future__ import annotations
import math
from optimization_system.models.experiment import StatisticalResults
from optimization_system.utils.statistics_utils import mean, std_dev, t_test
class ExperimentAnalyzer:
    def calculate_p_value(self,c,t): return t_test(c,t)
    def calculate_confidence_interval(self,values,confidence=0.95):
        if not values:return (0.0,0.0)
        m=mean(values);s=std_dev(values);margin=1.96*(s/math.sqrt(len(values))) if values else 0
        return (m-margin,m+margin)
    def calculate_effect_size(self,c,t):
        if not c or not t:return 0.0
        mc,mt=mean(c),mean(t);sc,st=std_dev(c),std_dev(t)
        pooled=math.sqrt(((len(c)-1)*sc*sc+(len(t)-1)*st*st)/max(1,len(c)+len(t)-2))
        return (mt-mc)/pooled if pooled else 0.0
    def is_significant(self,p_value,alpha=0.05): return p_value<alpha
    def determine_winner(self,e):
        k=e.metrics_to_compare[0] if e.metrics_to_compare else 'latency_ms'
        c=e.statistical_results.control_mean.get(k,0);t=e.statistical_results.treatment_mean.get(k,0)
        return 'treatment_wins' if t<c else 'control_wins' if c<t else 'no_difference'
    def analyze(self,e):
        sr=StatisticalResults()
        for m in e.metrics_to_compare:
            cv=[x.get(m,0.0) for x in e.control_results];tv=[x.get(m,0.0) for x in e.treatment_results]
            sr.control_mean[m]=mean(cv);sr.treatment_mean[m]=mean(tv)
            sr.difference_percent[m]=((sr.treatment_mean[m]-sr.control_mean[m])/sr.control_mean[m]*100 if sr.control_mean[m] else 0)
            p=self.calculate_p_value(cv,tv);sr.p_value[m]=p;sr.confidence_interval[m]=self.calculate_confidence_interval(tv);sr.is_significant[m]=self.is_significant(p);sr.effect_size[m]=self.calculate_effect_size(cv,tv)
        e.statistical_results=sr;e.conclusion=self.determine_winner(e);return sr
