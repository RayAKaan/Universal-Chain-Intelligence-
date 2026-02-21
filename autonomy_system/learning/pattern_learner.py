from __future__ import annotations
class PatternLearner:
    def learn_patterns(self,records): return [{'pattern':'high success with fast_processor','count':len(records)}] if records else []
    def get_success_patterns(self,goal_type): return [{'goal_type':goal_type,'pattern':'use adaptive strategy'}]
    def get_failure_patterns(self,goal_type): return [{'goal_type':goal_type,'pattern':'avoid overloaded capability'}]
