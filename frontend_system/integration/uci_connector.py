
from __future__ import annotations
from datetime import datetime, timezone
from uuid import uuid4
import random

class UCIConnector:
    def __init__(self, intelligence_core=None):
        self.core = intelligence_core
        self.mock = intelligence_core is None
        self.goals=[]
        self.capabilities=[]
        self.plans=[]
        self.improvements=[]
        self.notifications=[]
        self.timeline=[]
        self._seed()

    def _seed(self):
        if not self.mock:return
        now=datetime.now(timezone.utc).isoformat()
        for n,t in [("fast_processor","compute"),("report_generator","service"),("trainer","ml")]:
            self.capabilities.append({"id":str(uuid4()),"name":n,"type":t,"health":"healthy","latency_ms":random.randint(20,120),"reliability":round(random.uniform(0.9,0.99),3),"usage":random.randint(10,200),"updated_at":now})
        for txt,p in [("Analyze logs",70),("Train model",50)]:
            gid=str(uuid4()); pid=str(uuid4())
            self.goals.append({"record_id":gid,"goal":txt,"priority":p,"status":"active","submitted_at":now,"plan_id":pid,"progress":random.randint(10,80)})
            self.plans.append({"id":pid,"goal_id":gid,"name":f"Plan for {txt}","status":"running","steps":[{"id":"s1","name":"prepare"},{"id":"s2","name":"execute"}]})
        self.improvements=[{"id":str(uuid4()),"name":"Swap processor","impact":0.22,"status":"applied","timestamp":now}]
        self.notifications=[{"id":str(uuid4()),"message":"System booted","type":"info","unread":True,"timestamp":now}]
        self.timeline=[{"id":str(uuid4()),"phase":"phase5","event_type":"UCI_INITIALIZED","timestamp":now,"details":"System initialized"}]

    def _add_event(self,phase,event,details):
        self.timeline.append({"id":str(uuid4()),"phase":phase,"event_type":event,"timestamp":datetime.now(timezone.utc).isoformat(),"details":details})

    def _sync_from_core(self):
        if self.mock or not self.core:
            return
        try:
            for item in getattr(self.core.goal_manager, 'history', []):
                record = {
                    'record_id': item.record_id,
                    'goal': item.raw_input,
                    'priority': item.priority,
                    'status': item.status.value.lower(),
                    'submitted_at': item.submitted_at.isoformat() if getattr(item, 'submitted_at', None) else datetime.now(timezone.utc).isoformat(),
                    'plan_id': getattr(item, 'plan_id', ''),
                    'progress': 100 if getattr(item, 'status', None) and item.status.value.lower() == 'completed' else 0,
                }
                if not any(g['record_id'] == record['record_id'] for g in self.goals):
                    self.goals.insert(0, record)
        except Exception:
            return

    def get_system_status(self):
        self._sync_from_core()
        if not self.mock and self.core:
            s = self.core.get_status()
            status_name = s.overall_status.value.lower() if hasattr(s.overall_status, 'value') else str(s.overall_status).lower()
            return {
                "status": status_name,
                "overall_status": status_name,
                "score": round(getattr(s, 'overall_score', 0.0), 3),
                "autonomy": getattr(s, 'autonomy_level', 'guided'),
                "uptime_seconds": int(getattr(s, 'uptime_seconds', 0)),
                "phases": {k: getattr(v, 'status', 'unknown') for k, v in getattr(s, 'phase_status', {}).items()},
                "resources": {
                    "cpu": getattr(getattr(s, 'resource_status', None), 'cpu_percent', 0),
                    "memory": getattr(getattr(s, 'resource_status', None), 'memory_percent', 0),
                    "disk": getattr(getattr(s, 'resource_status', None), 'disk_percent', 0),
                },
                "active_goals": len(getattr(s, 'active_goals', []) or []),
                "running_goals": len(getattr(s, 'active_goals', []) or []),
            }
        return {"status":"healthy","score":0.96,"autonomy":"guided","uptime_seconds":7200,"phases":{f"phase{i}":"healthy" for i in range(7)},"resources":{"cpu":34,"memory":52,"disk":41},"active_goals":len([g for g in self.goals if g['status'] in ('active','queued')])}
    def get_dashboard_data(self):
        self._sync_from_core()
        if not self.mock and self.core:
            st = self.get_system_status()
            caps = self.get_capabilities()
            return {
                **st,
                "capability_count": len(caps),
                "improvements_applied": len(self.improvements),
                "recent_activity": self.get_timeline(limit=10),
                "goal_breakdown": {
                    "active": len([g for g in self.goals if g['status'] == 'active']),
                    "completed": len([g for g in self.goals if g['status'] == 'completed']),
                    "failed": len([g for g in self.goals if g['status'] == 'failed']),
                    "queued": len([g for g in self.goals if g['status'] == 'queued']),
                },
                "safety": {"alignment_score": 0.9, "trust_tier": "GUIDED", "violations_24h": 0},
            }
        st=self.get_system_status();
        return {**st,"capability_count":len(self.capabilities),"improvements_applied":len(self.improvements),"recent_activity":self.timeline[-10:],"goal_breakdown":{"active":len([g for g in self.goals if g['status']=='active']),"completed":len([g for g in self.goals if g['status']=='completed']),"failed":len([g for g in self.goals if g['status']=='failed']),"queued":len([g for g in self.goals if g['status']=='queued'] )},"safety":{"alignment_score":0.91,"trust_tier":"TRUSTED","violations_24h":0}}
    def get_health(self):
        if not self.mock and self.core:
            s = self.core.get_status()
            status_name = s.overall_status.value.lower() if hasattr(s.overall_status, 'value') else str(s.overall_status).lower()
            return {
                "healthy": status_name in ('healthy', 'degraded'),
                "score": round(getattr(s, 'overall_score', 0.0), 3),
                "phases": {k: {"health": getattr(v, 'status', 'unknown'), "score": getattr(v, 'score', 0)} for k, v in getattr(s, 'phase_status', {}).items()},
            }
        return {"healthy":True,"score":0.96,"phases":{f"phase{i}":{"health":"healthy","score":0.95} for i in range(7)}}
    def submit_goal(self,goal_text,priority):
        if not self.mock and self.core:
            from autonomy_system.models.goal_record import GoalSource
            rec = self.core.submit_goal(goal_text, GoalSource.EXTERNAL_API, int(priority))
            self._sync_from_core()
            self._add_event('phase5', 'GOAL_SUBMITTED', goal_text)
            return {"record_id": rec.record_id, "status": rec.status.value.lower()}
        gid=str(uuid4());pid=str(uuid4());now=datetime.now(timezone.utc).isoformat()
        g={"record_id":gid,"goal":goal_text,"priority":priority,"status":"queued","submitted_at":now,"plan_id":pid,"progress":0}
        self.goals.insert(0,g); self.plans.insert(0,{"id":pid,"goal_id":gid,"name":f"Plan for {goal_text}","status":"queued","steps":[{"id":"s1","name":"interpret"},{"id":"s2","name":"execute"}]})
        self.notifications.insert(0,{"id":str(uuid4()),"message":f"Goal queued: {goal_text}","type":"goal","unread":True,"timestamp":now})
        self._add_event('phase5','GOAL_SUBMITTED',goal_text)
        return {"record_id":gid,"status":"queued"}
    def get_goals(self,filters=None):
        self._sync_from_core()
        filters=filters or {}
        out=self.goals
        if filters.get('status'): out=[g for g in out if g['status']==filters['status']]
        return out
    def get_goal(self,goal_id):
        self._sync_from_core()
        g=next((x for x in self.goals if x['record_id']==goal_id),None)
        if not g:return {}
        p=next((x for x in self.plans if x['id']==g.get('plan_id')),{})
        return {"goal":g,"plan":p,"progress":{"percent":g.get('progress',0)}}
    def cancel_goal(self,goal_id):
        if not self.mock and self.core and hasattr(self.core, 'goal_manager'):
            ok = self.core.goal_manager.cancel(goal_id)
            self._sync_from_core()
            return ok
        for g in self.goals:
            if g['record_id']==goal_id:g['status']='cancelled';return True
        return False
    def pause_goal(self,goal_id):
        if not self.mock and self.core and hasattr(self.core, 'goal_manager'):
            ok = self.core.goal_manager.pause(goal_id)
            self._sync_from_core()
            return ok
        for g in self.goals:
            if g['record_id']==goal_id:g['status']='paused';return True
        return False
    def resume_goal(self,goal_id):
        if not self.mock and self.core and hasattr(self.core, 'goal_manager'):
            ok = self.core.goal_manager.resume(goal_id)
            self._sync_from_core()
            return ok
        for g in self.goals:
            if g['record_id']==goal_id:g['status']='active';return True
        return False
    def get_capabilities(self,filters=None):
        if not self.mock and self.core:
            out = []
            for c in self.core.get_capabilities():
                out.append({
                    'id': c.get('capability_id') or c.get('id') or str(uuid4()),
                    'name': c.get('name', 'unknown'),
                    'type': c.get('capability_type', c.get('type', 'general')).lower(),
                    'health': c.get('health_status', c.get('health', 'healthy')).lower(),
                    'latency_ms': c.get('metadata', {}).get('latency_ms', 0) if isinstance(c.get('metadata', {}), dict) else c.get('latency_ms', 0),
                    'reliability': c.get('metadata', {}).get('reliability', 1.0) if isinstance(c.get('metadata', {}), dict) else c.get('reliability', 1.0),
                    'usage': c.get('usage', 0),
                    'updated_at': datetime.now(timezone.utc).isoformat(),
                })
            self.capabilities = out
        f=filters or {}; out=self.capabilities
        if f.get('search'): out=[c for c in out if f['search'].lower() in c['name'].lower()]
        if f.get('type'): out=[c for c in out if c['type']==f['type']]
        return out
    def get_capability(self,capability_id):
        c=next((x for x in self.capabilities if x['id']==capability_id),None)
        return {"capability":c or {},"performance":{"p95_latency":c.get('latency_ms',0) if c else 0},"history":[]}
    def get_capability_summary(self):
        return {"total":len(self.capabilities),"by_type":{t:len([c for c in self.capabilities if c['type']==t]) for t in set(c['type'] for c in self.capabilities)}}
    def trigger_discovery(self): return {"status":"started","discovered":0}
    def trigger_benchmark(self,capability_id): return {"status":"started","capability_id":capability_id}
    def get_plans(self):
        self._sync_from_core()
        return self.plans
    def get_plan(self,plan_id): return next((p for p in self.plans if p['id']==plan_id),{})
    def get_plan_graph(self,plan_id):
        p=self.get_plan(plan_id); steps=p.get('steps',[])
        nodes=[{"id":s['id'],"label":s['name'],"status":"done" if i==0 else "running"} for i,s in enumerate(steps)]
        edges=[{"from":steps[i]['id'],"to":steps[i+1]['id']} for i in range(len(steps)-1)]
        return {"nodes":nodes,"edges":edges}
    def build_from_spec(self,spec): return {"build_id":str(uuid4()),"status":"building","spec":spec}
    def get_artifacts(self): return [{"id":str(uuid4()),"name":"artifact.py","type":"python"}]
    def get_templates(self): return [{"id":"api","name":"API Endpoint"},{"id":"worker","name":"Worker"}]
    def get_build_history(self): return []
    def get_improvements(self): return self.improvements
    def get_bottlenecks(self): return [{"name":"slow_processor","severity":"high"}]
    def get_opportunities(self): return [{"name":"cache responses","estimated_gain":0.18}]
    def get_improvement_impact(self): return {"cumulative":0.32,"count":len(self.improvements)}
    def trigger_improvement_cycle(self): return {"status":"triggered"}
    def get_safety_status(self): return {"status":"nominal","alignment":0.91,"containment":"intact","emergency":False}
    def get_audit_trail(self,limit,offset): return [{"seq":i+1+offset,"action":"execute_goal","outcome":"allowed"} for i in range(limit)]
    def get_trust_level(self): return {"tier":"TRUSTED","score":0.86,"history":[]}
    def get_alignment_score(self): return {"overall":0.91,"dimensions":{"helpfulness":0.93,"honesty":0.95}}
    def get_violations(self): return []
    def activate_panic_mode(self,reason): self._add_event('phase6','PANIC_MODE',reason); return True
    def deactivate_panic_mode(self,authorization): return authorization=='human_authorized'
    def get_settings(self):
        level = 'guided'
        if not self.mock and self.core and hasattr(self.core, 'autonomy_controller'):
            level = self.core.autonomy_controller.get_level().name.lower()
        return {"autonomy":level,"theme":"dark","refresh_ms":5000}
    def set_autonomy_level(self,level):
        self._add_event('phase5','AUTONOMY_LEVEL_CHANGED',level)
        if not self.mock and self.core:
            self.core.set_autonomy_level(level.upper())
        return True
    def update_config(self,updates): return True
    def query_knowledge(self,query):
        if not self.mock and self.core and hasattr(self.core, 'knowledge_base'):
            return [e.__dict__ for e in self.core.knowledge_base.query(**(query or {}))]
        return [{"subject":"uci","predicate":"has_mode","object":"guided","confidence":1.0}]
    def add_knowledge(self,entry): return str(uuid4())
    def execute_command(self,command):
        if command=='status': return {"output":str(self.get_system_status()),"type":"text"}
        if command.startswith('goal '): return {"output":str(self.submit_goal(command[5:],50)),"type":"text"}
        return {"output":f"Executed: {command}","type":"text"}
    def ask_system(self,question): return f"I can help with goals, planning, construction, optimization, and safety. Question: {question}"
    def get_system_info(self): return {"name":"Universal Chain Intelligence","version":"1.0.0","phases":7}
    def shutdown(self): return True
    def get_notifications(self): return self.notifications[:]
    def get_unread_count(self): return len([n for n in self.notifications if n.get('unread')])
    def mark_read(self,notification_id):
        for n in self.notifications:
            if n['id']==notification_id:n['unread']=False;return True
        return False
    def get_timeline(self,since=None,limit=100,phase=None):
        out=self.timeline
        if phase: out=[e for e in out if e.get('phase')==phase]
        return out[-limit:]

    def get_version_info(self):
        mode = 'mock' if self.mock else 'connected'
        return {
            'name': 'Universal Chain Intelligence Frontend API',
            'api_version': '1.0.0',
            'mode': mode,
            'backend': 'autonomy_system' if not self.mock else 'in_memory_mock',
        }

    def get_api_contracts(self):
        return {
            'status': {
                'required': ['status', 'active_goals'],
                'optional': ['overall_status', 'running_goals', 'resources', 'autonomy'],
            },
            'goals': {
                'required': ['goals', 'total'],
                'item_required': ['record_id', 'goal', 'status', 'priority'],
            },
            'health_resources': {
                'required_any_of': [['cpu', 'cpu_percent'], ['memory', 'memory_percent'], ['disk', 'disk_percent']],
            },
            'capabilities': {
                'required': ['capabilities'],
                'item_optional': ['id', 'name', 'type', 'health', 'latency_ms', 'reliability'],
            },
        }
