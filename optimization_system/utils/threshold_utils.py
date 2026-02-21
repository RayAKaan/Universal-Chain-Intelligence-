from __future__ import annotations
from optimization_system.utils.statistics_utils import mean,std_dev

def adaptive_threshold(values,sensitivity=2.0): return mean(values)+sensitivity*std_dev(values) if values else 0.0
def check_threshold(value,threshold,operator): return {'gt':value>threshold,'lt':value<threshold,'gte':value>=threshold,'lte':value<=threshold}.get(operator,False)
def dynamic_threshold(historical_values,current_value): return current_value>adaptive_threshold(historical_values,2.0) if historical_values else False
