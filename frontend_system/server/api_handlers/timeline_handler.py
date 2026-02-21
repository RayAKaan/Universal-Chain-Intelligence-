from frontend_system.server.api_handlers.base_handler import BaseAPIHandler
class TimelineHandler(BaseAPIHandler):
    def list(self,q):
        return self.ok({'events':self.uci.get_timeline(q.get('since'),int(q.get('limit',100)),q.get('phase'))})
