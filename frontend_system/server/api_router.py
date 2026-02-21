
from urllib.parse import urlparse, parse_qs
from frontend_system.server.api_handlers.goal_handler import GoalHandler
from frontend_system.server.api_handlers.status_handler import StatusHandler
from frontend_system.server.api_handlers.capability_handler import CapabilityHandler
from frontend_system.server.api_handlers.plan_handler import PlanHandler
from frontend_system.server.api_handlers.construction_handler import ConstructionHandler
from frontend_system.server.api_handlers.improvement_handler import ImprovementHandler
from frontend_system.server.api_handlers.safety_handler import SafetyHandler
from frontend_system.server.api_handlers.settings_handler import SettingsHandler
from frontend_system.server.api_handlers.knowledge_handler import KnowledgeHandler
from frontend_system.server.api_handlers.notification_handler import NotificationHandler
from frontend_system.server.api_handlers.timeline_handler import TimelineHandler
from frontend_system.server.api_handlers.health_handler import HealthHandler
from frontend_system.server.api_handlers.console_handler import ConsoleHandler

class APIRouter:
    def __init__(self, connector):
        self.h={
            'goals':GoalHandler(connector),'status':StatusHandler(connector),'capabilities':CapabilityHandler(connector),
            'plans':PlanHandler(connector),'construction':ConstructionHandler(connector),'improvements':ImprovementHandler(connector),
            'safety':SafetyHandler(connector),'settings':SettingsHandler(connector),'knowledge':KnowledgeHandler(connector),
            'notifications':NotificationHandler(connector),'timeline':TimelineHandler(connector),'health':HealthHandler(connector),
            'console':ConsoleHandler(connector)
        }
        self.connector=connector

    def _q(self,path):
        return {k:v[-1] for k,v in parse_qs(urlparse(path).query).items()}

    def route(self, method, path, payload):
        pure=urlparse(path).path
        parts=[p for p in pure.split('/') if p]
        q=self._q(path)
        if pure=='/api/status': return self.h['status'].status()
        if pure=='/api/status/health': return self.h['status'].health()
        if pure=='/api/status/dashboard': return self.h['status'].dashboard()
        if pure=='/api/system/info': return 200, self.connector.get_system_info()
        if pure=='/api/system/ask': return 200, {'answer': self.connector.ask_system(q.get('q',''))}
        if pure=='/api/system/shutdown' and method=='POST': return 200, {'ok': self.connector.shutdown()}
        if parts[:2]==['api','goals']:
            h=self.h['goals']
            if len(parts)==2 and method=='POST': return h.submit(payload)
            if len(parts)==2 and method=='GET': return h.list(q)
            if len(parts)==3 and parts[2]=='history': return h.list(q)
            if len(parts)>=3:
                gid=parts[2]
                if len(parts)==3 and method=='GET': return h.detail(gid)
                if len(parts)==4 and parts[3]=='cancel': return h.cancel(gid)
                if len(parts)==4 and parts[3]=='pause': return h.pause(gid)
                if len(parts)==4 and parts[3]=='resume': return h.resume(gid)
        if parts[:2]==['api','capabilities']:
            h=self.h['capabilities']
            if len(parts)==2: return h.list(q)
            if len(parts)==3 and parts[2]=='summary': return h.summary()
            if len(parts)==3 and parts[2]=='discover' and method=='POST': return h.discover()
            if len(parts)==4 and parts[2]=='benchmark' and method=='POST': return h.benchmark(parts[3])
            if len(parts)==3: return h.detail(parts[2])
        if parts[:2]==['api','plans']:
            h=self.h['plans']
            if len(parts)==2: return h.list()
            if len(parts)==3: return h.detail(parts[2])
            if len(parts)==4 and parts[3]=='graph': return h.graph(parts[2])
            if len(parts)==4 and parts[3]=='progress': return h.progress(parts[2])
        if parts[:2]==['api','construction']:
            h=self.h['construction']
            if pure=='/api/construction/build' and method=='POST': return h.build(payload)
            if pure=='/api/construction/artifacts': return h.artifacts()
            if pure=='/api/construction/templates': return h.templates()
            if pure=='/api/construction/history': return h.history()
        if parts[:2]==['api','improvements']:
            h=self.h['improvements']
            m={
                '/api/improvements':h.list,'/api/improvements/active':h.active,'/api/improvements/history':h.history,
                '/api/improvements/impact':h.impact,'/api/improvements/bottlenecks':h.bottlenecks,'/api/improvements/opportunities':h.opportunities
            }
            if pure=='/api/improvements/cycle' and method=='POST': return h.cycle()
            if pure in m: return m[pure]()
        if parts[:2]==['api','safety']:
            h=self.h['safety']
            m={'/api/safety/status':h.status,'/api/safety/audit':lambda:h.audit(q),'/api/safety/trust':h.trust,'/api/safety/alignment':h.alignment,'/api/safety/violations':h.violations,'/api/safety/containment':h.containment}
            if pure=='/api/safety/emergency/panic' and method=='POST': return h.panic(payload)
            if pure=='/api/safety/emergency/reset' and method=='POST': return h.reset(payload)
            if pure in m: return m[pure]()
        if parts[:2]==['api','settings']:
            h=self.h['settings']
            if pure=='/api/settings' and method=='GET': return h.get()
            if pure=='/api/settings/autonomy' and method=='POST': return h.autonomy(payload)
            if pure=='/api/settings/config' and method=='POST': return h.config(payload)
            if pure=='/api/settings/autonomy/levels': return h.levels()
        if parts[:2]==['api','knowledge']:
            h=self.h['knowledge']
            if pure=='/api/knowledge' and method=='GET': return h.query(q)
            if pure=='/api/knowledge' and method=='POST': return h.add(payload)
            if pure=='/api/knowledge/stats': return h.stats()
        if parts[:2]==['api','notifications']:
            h=self.h['notifications']
            if pure=='/api/notifications' and method=='GET': return h.list(q)
            if pure=='/api/notifications/count' and method=='GET': return h.count()
            if len(parts)==4 and parts[3]=='read' and method=='POST': return h.read(parts[2])
        if pure=='/api/timeline': return self.h['timeline'].list(q)
        if pure=='/api/console/execute' and method=='POST': return self.h['console'].execute(payload)
        if pure=='/api/console/commands': return self.h['console'].commands()
        if pure=='/api/health/realtime': return self.h['health'].realtime()
        if pure=='/api/health/phases': return self.h['health'].phases()
        if pure=='/api/health/resources': return self.h['health'].resources()
        if pure=='/api/health/history': return self.h['health'].history()
        return 404, {'error':'not found'}
