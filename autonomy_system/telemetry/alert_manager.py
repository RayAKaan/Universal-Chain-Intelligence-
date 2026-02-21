from __future__ import annotations
import uuid
class AlertManager:
    def __init__(self): self.rules=[]; self.active=[]; self._defaults()
    def _defaults(self):
        self.register_alert_rule('System unhealthy',lambda pts:any(getattr(p,'name','')=='overall_score' and p.value<0.5 for p in pts),'high','System health low')
        self.register_alert_rule('Resource usage > 90%',lambda pts:any(getattr(p,'name','')=='cpu_percent' and p.value>90 for p in pts),'high','CPU high')
        self.register_alert_rule('Goal failure rate > 20%',lambda pts:False,'medium','Goal failures high')
        self.register_alert_rule('Capability degradation',lambda pts:False,'medium','Capability degraded')
        self.register_alert_rule('Improvement regression detected',lambda pts:False,'high','Regression detected')
        self.register_alert_rule('Background service stopped',lambda pts:False,'high','Service stopped')
    def register_alert_rule(self,name,condition,severity,message_template): self.rules.append({'name':name,'condition':condition,'severity':severity,'template':message_template})
    def check_alerts(self,telemetry):
        found=[]
        for r in self.rules:
            if r['condition'](telemetry):
                a={'alert_id':str(uuid.uuid4()),'name':r['name'],'severity':r['severity'],'message':r['template']}
                self.active.append(a); found.append(a)
        return found
    def get_active_alerts(self): return self.active
    def acknowledge_alert(self,alert_id): self.active=[a for a in self.active if a['alert_id']!=alert_id]
