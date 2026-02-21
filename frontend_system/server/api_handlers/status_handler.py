from frontend_system.server.api_handlers.base_handler import BaseAPIHandler
class StatusHandler(BaseAPIHandler):
    def status(self): return self.ok(self.uci.get_system_status())
    def health(self): return self.ok(self.uci.get_health())
    def dashboard(self): return self.ok(self.uci.get_dashboard_data())
