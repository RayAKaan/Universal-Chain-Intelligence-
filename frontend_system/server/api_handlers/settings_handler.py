from frontend_system.server.api_handlers.base_handler import BaseAPIHandler
class SettingsHandler(BaseAPIHandler):
    def get(self): return self.ok(self.uci.get_settings())
    def autonomy(self,p): return self.ok({'ok':self.uci.set_autonomy_level(p.get('level','guided'))})
    def config(self,p): return self.ok({'ok':self.uci.update_config(p)})
    def levels(self): return self.ok({'levels':['passive','guided','autonomous']})
