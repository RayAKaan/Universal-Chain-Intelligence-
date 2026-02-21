from __future__ import annotations
class PhaseTuner:
    def __init__(self): self.current={}; self.history=[]
    def tune_phase(self,phase_name,parameters): self.current.setdefault(phase_name,{}).update(parameters); self.history.append({'phase':phase_name,'parameters':parameters}); return {'phase':phase_name,'applied':parameters}
    def get_current_tuning(self): return self.current
    def get_tuning_history(self): return self.history
    def reset_to_defaults(self): self.current={}
