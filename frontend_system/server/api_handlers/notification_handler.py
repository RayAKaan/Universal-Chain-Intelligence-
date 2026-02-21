from frontend_system.server.api_handlers.base_handler import BaseHandler
class NotificationHandler(BaseHandler):
    def list(self,q):
        n=self.uci.get_notifications()
        if q.get('unread')=='true': n=[x for x in n if x.get('unread')]
        return self.ok({'notifications':n})
    def read(self,nid): return self.ok({'ok':self.uci.mark_read(nid)})
    def count(self): return self.ok({'unread':self.uci.get_unread_count()})
