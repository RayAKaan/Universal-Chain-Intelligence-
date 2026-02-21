from frontend_system.server.api_handlers.base_handler import BaseHandler
class SafetyHandler(BaseHandler):
    def status(self): return self.ok(self.uci.get_safety_status())
    def audit(self,q):
        l=int(q.get('limit',100));o=int(q.get('offset',0));return self.ok({'audit':self.uci.get_audit_trail(l,o)})
    def trust(self): return self.ok(self.uci.get_trust_level())
    def alignment(self): return self.ok(self.uci.get_alignment_score())
    def violations(self): return self.ok({'violations':self.uci.get_violations()})
    def containment(self): return self.ok(self.uci.get_safety_status())
    def panic(self,p): return self.ok({'ok':self.uci.activate_panic_mode(p.get('reason','manual'))})
    def reset(self,p): return self.ok({'ok':self.uci.deactivate_panic_mode(p.get('authorization',''))})
