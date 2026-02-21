from frontend_system.server.api_handlers.base_handler import BaseHandler
class KnowledgeHandler(BaseHandler):
    def query(self,q): return self.ok({'entries':self.uci.query_knowledge(q)})
    def add(self,p): return self.ok({'entry_id':self.uci.add_knowledge(p)})
    def stats(self): return self.ok({'stats':{'total':len(self.uci.query_knowledge({}))}})
