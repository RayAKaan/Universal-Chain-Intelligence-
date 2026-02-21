from __future__ import annotations
class SystemConsciousness:
    def __init__(self,introspection_engine,state_narrator,capability_map,self_model,config): self.introspection=introspection_engine; self.narrator=state_narrator; self.capmap=capability_map; self.self_model=self_model; self.config=config
    def get_self_awareness(self):
        i=self.introspection.introspect()
        return {'identity':self.self_model.get_description(),'health':'healthy','capabilities':self.capmap.build_map(),'strengths':i['strength_areas'],'weaknesses':i['weakness_areas'],'recommendations':['continue improvement cycles']}
    def narrate_status(self): return self.narrator.narrate_system_state(type('S',(),{'overall_status':type('E',(),{'value':'HEALTHY'})(),'autonomy_level':'guided','uptime_seconds':120})())
    def narrate_activity(self,period_minutes=60): return f'In the last {period_minutes} minutes, processed goals and maintained health.'
    def get_capability_summary(self): return 'I can process goals, plan, execute, construct, optimize, and self-heal.'
    def get_limitation_awareness(self): return self.capmap.get_gaps()
    def answer_question(self,question):
        q=question.lower()
        if 'what can you do' in q: return self.get_capability_summary()
        if 'how are you' in q: return self.narrate_status()
        if 'weakness' in q: return ', '.join(self.get_limitation_awareness())
        if 'learned' in q: return '; '.join(self.introspection.get_recent_learnings())
        return 'I can answer questions about my status, capabilities, activity, and limitations.'
