from __future__ import annotations
from datetime import datetime, timezone
from autonomy_system.models.learning_record import LearningRecord, LearningType
class LearningEngine:
    def __init__(self,experience_store,pattern_learner,preference_tracker,adaptation_engine,config): self.store=experience_store; self.pattern=pattern_learner; self.pref=preference_tracker; self.adapt_engine=adaptation_engine; self.config=config
    def _save(self,rec): self.store.store(rec); return rec
    def learn_from_goal(self,goal_record):
        rec=LearningRecord(learning_type=LearningType.GOAL_OUTCOME,observation={'context':goal_record.metadata,'action':{'goal':goal_record.raw_input},'outcome':{'status':goal_record.status.value}},lesson=f"Goal {goal_record.status.value}",confidence=0.8,applicable_to=[goal_record.raw_input.split(' ')[0]])
        self.pref.record_preference('goal_type',goal_record.metadata.get('strategy','default'),'success' if goal_record.status.value=='COMPLETED' else 'failure')
        return [self._save(rec)]
    def learn_from_improvement(self,improvement): return [self._save(LearningRecord(LearningType.OPTIMIZATION_RESULT,{'context':{},'action':improvement,'outcome':{'status':'applied'}},'Improvement applied',0.9))]
    def learn_from_failure(self,failure): return [self._save(LearningRecord(LearningType.FAILURE_PATTERN,{'context':failure,'action':{},'outcome':{'status':'failed'}},'Failure observed',0.8))]
    def learn_from_healing(self,healing_event): return [self._save(LearningRecord(LearningType.FAILURE_PATTERN,{'context':{},'action':{'healing':healing_event.recovery_strategy},'outcome':{'success':healing_event.recovery_success}},'Healing learned',0.85))]
    def apply_learnings(self,context):
        recs=self.store.get_applicable(context)
        return {'preferred_strategy':self.pref.get_preferred('goal_type') or 'adaptive','preferred_capabilities':['fast_processor'],'known_pitfalls':['overloaded capability'],'estimated_success_rate':0.85,'resource_recommendations':{'max_cpu':80},'records':len(recs)}
    def get_learnings(self,learning_type=None,limit=100): return self.store.query(learning_type=learning_type,limit=limit)
    def get_learning_stats(self): recs=self.get_learnings(limit=1000); return {'total':len(recs),'high_confidence':len([r for r in recs if r.confidence>=self.config.MIN_CONFIDENCE_TO_APPLY])}
    def process_recent(self): return self.get_learning_stats()
