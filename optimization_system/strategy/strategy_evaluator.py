from __future__ import annotations
class StrategyEvaluator:
    def __init__(self,phase2_bridge): self.p2=phase2_bridge
    def evaluate_strategy(self,strategy_name):
        p=self.p2.get_strategy_performance().get(strategy_name,{'uses':0,'success_rate':0.8,'avg_plan_duration_ms':200})
        return {'strategy_name':strategy_name,'total_uses':p.get('uses',0),'success_rate':p.get('success_rate',0.8),'avg_plan_duration_ms':p.get('avg_plan_duration_ms',200),'avg_execution_duration_ms':400,'avg_plan_complexity':8,'best_for_goal_types':['general'],'worst_for_goal_types':[],'overall_score':p.get('success_rate',0.8)}
    def evaluate_all(self): return {n:self.evaluate_strategy(n) for n in self.p2.get_strategy_performance()}
    def compare_strategies(self,a,b,goal_type=None):
        ea,eb=self.evaluate_strategy(a),self.evaluate_strategy(b)
        return {'better':a if ea['overall_score']>=eb['overall_score'] else b,'delta':ea['overall_score']-eb['overall_score']}
    def get_strategy_recommendations(self,goal_type,domain):
        return sorted([(k,v['overall_score']) for k,v in self.evaluate_all().items()],key=lambda x:x[1],reverse=True)
