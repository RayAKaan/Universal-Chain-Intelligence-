from frontend_system.server.api_handlers.base_handler import BaseAPIHandler
class HealthHandler(BaseAPIHandler):
    def realtime(self): return self.ok(self.uci.get_health())
    def phases(self): return self.ok({'phases':self.uci.get_health().get('phases',{})})
    def resources(self):
        resources = self.uci.get_system_status().get('resources', {})
        normalized = {
            'cpu': resources.get('cpu', resources.get('cpu_percent', 0)),
            'memory': resources.get('memory', resources.get('memory_percent', 0)),
            'disk': resources.get('disk', resources.get('disk_percent', 0)),
            'cpu_percent': resources.get('cpu_percent', resources.get('cpu', 0)),
            'memory_percent': resources.get('memory_percent', resources.get('memory', 0)),
            'disk_percent': resources.get('disk_percent', resources.get('disk', 0)),
        }
        return self.ok({'resources': normalized})
    def history(self): return self.ok({'history':[self.uci.get_health()]})
