from frontend_system.server.api_handlers.base_handler import BaseHandler
class GoalHandler(BaseHandler):
    def submit(self,payload): return self.ok(self.uci.submit_goal(payload.get('goal',''),int(payload.get('priority',50))))
    def list(self,query):
        goals=self.uci.get_goals(query); return self.ok({'goals':goals,'total':len(goals)})
    def detail(self,gid): return self.ok(self.uci.get_goal(gid))
    def cancel(self,gid): return self.ok({'ok':self.uci.cancel_goal(gid)})
    def pause(self,gid): return self.ok({'ok':self.uci.pause_goal(gid)})
    def resume(self,gid): return self.ok({'ok':self.uci.resume_goal(gid)})
