from __future__ import annotations
from autonomy_system.communication.message_router import MessageRouter
from autonomy_system.communication.response_formatter import ResponseFormatter
from autonomy_system.communication.request_parser import RequestParser
class CommunicationHub:
    def __init__(self,message_router=None,response_formatter=None,request_parser=None,config=None): self.router=message_router or MessageRouter(); self.formatter=response_formatter or ResponseFormatter(); self.parser=request_parser or RequestParser(); self.config=config; self.adapters=[]
    def register_adapter(self,adapter): adapter.hub=self; self.adapters.append(adapter)
    def start(self):
        for a in self.adapters: a.start()
    def stop(self):
        for a in self.adapters: a.stop()
    def handle_message(self,message):
        return self.router.route(message)
    def send_notification(self,message,severity='info'):
        for a in self.adapters:
            if a.is_running():
                try:a.send({'severity':severity,'message':message})
                except Exception: pass
