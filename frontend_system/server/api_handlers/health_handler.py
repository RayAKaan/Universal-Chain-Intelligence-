from frontend_system.server.api_handlers.base_handler import BaseHandler
class HealthHandler(BaseHandler):
    def realtime(self): return self.ok(self.uci.get_health())
    def phases(self): return self.ok({'phases':self.uci.get_health().get('phases',{})})
    def resources(self): return self.ok({'resources':self.uci.get_system_status().get('resources',{})})
    def history(self): return self.ok({'history':[self.uci.get_health()]})
