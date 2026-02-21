from frontend_system.server.api_handlers.base_handler import BaseAPIHandler
class ImprovementHandler(BaseAPIHandler):
    def list(self): return self.ok({'improvements':self.uci.get_improvements()})
    def active(self): return self.ok({'active':[i for i in self.uci.get_improvements() if i.get('status')!='applied']})
    def history(self): return self.ok({'history':self.uci.get_improvements()})
    def impact(self): return self.ok(self.uci.get_improvement_impact())
    def cycle(self): return self.ok(self.uci.trigger_improvement_cycle())
    def bottlenecks(self): return self.ok({'bottlenecks':self.uci.get_bottlenecks()})
    def opportunities(self): return self.ok({'opportunities':self.uci.get_opportunities()})
