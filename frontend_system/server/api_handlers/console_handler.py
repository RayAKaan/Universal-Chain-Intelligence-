from frontend_system.server.api_handlers.base_handler import BaseHandler
class ConsoleHandler(BaseHandler):
    def execute(self,p): return self.ok(self.uci.execute_command(p.get('command','')))
    def commands(self): return self.ok({'commands':['status','goals','goal <text>','capabilities','health','improvements','safety','ask <q>','autonomy <level>','help','clear']})
