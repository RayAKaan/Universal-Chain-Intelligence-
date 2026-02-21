from __future__ import annotations
class SelfModificationEngine:
    def __init__(self,modification_planner,modification_applier,modification_validator,rollback_engine,safety_governor,config): self.planner=modification_planner;self.applier=modification_applier;self.validator=modification_validator;self.rollback_engine=rollback_engine;self.safety=safety_governor;self.config=config;self.history=[]
    def apply_modification(self,modification):
        if not self.safety.evaluate_modification(modification).is_safe: return False
        ok,_=self.validator.validate_pre_apply(modification)
        if not ok:return False
        if not self.applier.apply(modification): self.rollback_engine.rollback(modification); return False
        ok2,_=self.validator.validate_post_apply(modification)
        if not ok2: self.rollback_engine.rollback(modification); return False
        self.history.append(modification); return True
    def apply_batch(self,modifications):
        out=[]
        for m in modifications:
            s=self.apply_modification(m);out.append(s)
            if not s: self.rollback_engine.rollback_batch([x for x,y in zip(modifications,out) if y]); break
        return out
    def rollback(self,modification_id):
        for m in self.history:
            if m.modification_id==modification_id:return self.rollback_engine.rollback(m)
        return False
    def rollback_to_baseline(self,baseline_id): return self.rollback_engine.rollback_batch(self.history)
    def get_modification_history(self): return list(self.history)
    def get_pending_modifications(self): return [m for m in self.history if not m.applied]
