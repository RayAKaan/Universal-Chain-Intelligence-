from frontend_system.server.api_handlers.base_handler import BaseHandler
class ConstructionHandler(BaseHandler):
    def build(self,p): return self.ok(self.uci.build_from_spec(p.get('spec',{})))
    def artifacts(self): return self.ok({'artifacts':self.uci.get_artifacts()})
    def templates(self): return self.ok({'templates':self.uci.get_templates()})
    def history(self): return self.ok({'history':self.uci.get_build_history()})
