from __future__ import annotations
class OversightManager:
    def __init__(self): self.decisions=[]
    def record_decision(self,action,autonomy_level,auto_approved,details): self.decisions.append({'action':action,'autonomy_level':str(autonomy_level),'auto_approved':auto_approved,'details':details})
    def get_decisions(self,limit=100): return self.decisions[-limit:]
    def get_approval_rate(self):
        if not self.decisions:return 0.0
        return len([d for d in self.decisions if d['auto_approved']])/len(self.decisions)
    def get_rejection_reasons(self): return [d['details'].get('reason','') for d in self.decisions if not d['auto_approved']]
