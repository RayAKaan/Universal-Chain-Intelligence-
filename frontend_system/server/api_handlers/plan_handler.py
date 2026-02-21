from frontend_system.server.api_handlers.base_handler import BaseAPIHandler
class PlanHandler(BaseAPIHandler):
    def list(self): return self.ok({'plans':self.uci.get_plans()})
    def detail(self,pid): return self.ok(self.uci.get_plan(pid))
    def graph(self,pid): return self.ok(self.uci.get_plan_graph(pid))
    def progress(self,pid):
        p=self.uci.get_plan(pid); return self.ok({'progress':50 if p else 0})
