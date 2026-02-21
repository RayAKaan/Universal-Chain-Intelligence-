from frontend_system.server.api_handlers.base_handler import BaseAPIHandler
class CapabilityHandler(BaseAPIHandler):
    def list(self,q):
        c=self.uci.get_capabilities(q); return self.ok({'capabilities':c,'total':len(c)})
    def detail(self,cid): return self.ok(self.uci.get_capability(cid))
    def summary(self): return self.ok(self.uci.get_capability_summary())
    def discover(self): return self.ok(self.uci.trigger_discovery())
    def benchmark(self,cid): return self.ok(self.uci.trigger_benchmark(cid))
