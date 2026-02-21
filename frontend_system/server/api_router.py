
from urllib.parse import parse_qs, urlparse
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
        self.goal=GoalHandler(connector); self.status=StatusHandler(connector); self.cap=CapabilityHandler(connector)
        self.plan=PlanHandler(connector); self.cons=ConstructionHandler(connector); self.imp=ImprovementHandler(connector)
        self.safe=SafetyHandler(connector); self.sett=SettingsHandler(connector); self.k=KnowledgeHandler(connector)
        self.n=NotificationHandler(connector); self.t=TimelineHandler(connector); self.h=HealthHandler(connector)
        self.c=ConsoleHandler(connector); self.connector=connector

    def _parts(self,path): return [p for p in path.split('/') if p]
    def _query(self,path):
        qs=parse_qs(urlparse(path).query); return {k:v[-1] for k,v in qs.items()}

    def route(self, method, path, payload):
        pure=urlparse(path).path
        q=self._query(path)
        parts=self._parts(pure)
        if pure=='/api/status': return self.status.status()
        if pure=='/api/status/health': return self.status.health()
        if pure=='/api/status/dashboard': return self.status.dashboard()
        if pure=='/api/goals' and method=='POST': return self.goal.submit(payload)
        if pure=='/api/goals' and method=='GET': return self.goal.list(q)
        if pure=='/api/goals/history': return self.goal.list(q)
        if len(parts)>=3 and parts[0]=='api' and parts[1]=='goals':
            gid=parts[2]
            if len(parts)==3 and method=='GET': return self.goal.detail(gid)
            if parts[-1]=='cancel': return self.goal.cancel(gid)
            if parts[-1]=='pause': return self.goal.pause(gid)
            if parts[-1]=='resume': return self.goal.resume(gid)
        if pure=='/api/capabilities' and method=='GET': return self.cap.list(q)
        if pure=='/api/capabilities/summary': return self.cap.summary()
        if pure=='/api/capabilities/discover' and method=='POST': return self.cap.discover()
        if len(parts)>=4 and parts[:3]==['api','capabilities','benchmark'] and method=='POST': return self.cap.benchmark(parts[3])
        if len(parts)==3 and parts[:2]==['api','capabilities']: return self.cap.detail(parts[2])
        if pure=='/api/plans': return self.plan.list()
        if len(parts)>=3 and parts[:2]==['api','plans']:
            pid=parts[2]
            if len(parts)==3:return self.plan.detail(pid)
            if parts[3]=='graph': return self.plan.graph(pid)
            if parts[3]=='progress': return self.plan.progress(pid)
        if pure=='/api/construction/build' and method=='POST': return self.cons.build(payload)
        if pure=='/api/construction/artifacts': return self.cons.artifacts()
        if pure=='/api/construction/templates': return self.cons.templates()
        if pure=='/api/construction/history': return self.cons.history()
        if pure=='/api/improvements': return self.imp.list()
        if pure=='/api/improvements/active': return self.imp.active()
        if pure=='/api/improvements/history': return self.imp.history()
        if pure=='/api/improvements/impact': return self.imp.impact()
        if pure=='/api/improvements/cycle' and method=='POST': return self.imp.cycle()
        if pure=='/api/improvements/bottlenecks': return self.imp.bottlenecks()
        if pure=='/api/improvements/opportunities': return self.imp.opportunities()
        if pure=='/api/safety/status': return self.safe.status()
        if pure=='/api/safety/audit': return self.safe.audit(q)
        if pure=='/api/safety/trust': return self.safe.trust()
        if pure=='/api/safety/alignment': return self.safe.alignment()
        if pure=='/api/safety/violations': return self.safe.violations()
        if pure=='/api/safety/containment': return self.safe.containment()
        if pure=='/api/safety/emergency/panic' and method=='POST': return self.safe.panic(payload)
        if pure=='/api/safety/emergency/reset' and method=='POST': return self.safe.reset(payload)
        if pure=='/api/settings' and method=='GET': return self.sett.get()
        if pure=='/api/settings/autonomy' and method=='POST': return self.sett.autonomy(payload)
        if pure=='/api/settings/config' and method=='POST': return self.sett.config(payload)
        if pure=='/api/settings/autonomy/levels' and method=='GET': return self.sett.levels()
        if pure=='/api/knowledge' and method=='GET': return self.k.query(q)
        if pure=='/api/knowledge' and method=='POST': return self.k.add(payload)
        if pure=='/api/knowledge/stats': return self.k.stats()
        if pure=='/api/notifications' and method=='GET': return self.n.list(q)
        if pure=='/api/notifications/count' and method=='GET': return self.n.count()
        if len(parts)>=4 and parts[:2]==['api','notifications'] and parts[-1]=='read' and method=='POST': return self.n.read(parts[2])
        if pure=='/api/timeline': return self.t.list(q)
        if pure=='/api/console/execute' and method=='POST': return self.c.execute(payload)
        if pure=='/api/console/commands': return self.c.commands()
        if pure=='/api/health/realtime': return self.h.realtime()
        if pure=='/api/health/phases': return self.h.phases()
        if pure=='/api/health/resources': return self.h.resources()
        if pure=='/api/health/history': return self.h.history()
        if pure=='/api/system/info': return 200, self.connector.get_system_info()
        if pure=='/api/system/ask': return 200, {'answer':self.connector.ask_system(q.get('q',''))}
        if pure=='/api/system/shutdown' and method=='POST': return 200, {'ok':self.connector.shutdown()}
        return 404, {'error':'not found'}
