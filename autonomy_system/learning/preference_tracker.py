from __future__ import annotations
class PreferenceTracker:
    def __init__(self): self.data={}
    def record_preference(self,context,option,outcome): self.data.setdefault(context,{}).setdefault(option,{'wins':0,'total':0}); self.data[context][option]['total']+=1; self.data[context][option]['wins']+=1 if outcome=='success' else 0
    def get_preferred(self,context):
        opts=self.data.get(context,{})
        if not opts:return ''
        return max(opts,key=lambda o:(opts[o]['wins']/max(1,opts[o]['total'])))
    def get_preference_stats(self): return self.data
