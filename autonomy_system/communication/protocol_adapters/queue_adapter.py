from __future__ import annotations
from queue import Queue
from autonomy_system.communication.protocol_adapters.base_adapter import BaseAdapter
class QueueAdapter(BaseAdapter):
    name='queue'; protocol='queue'
    def __init__(self,hub=None): super().__init__(hub); self.q=Queue(); self.results={}
    def start(self): self.running=True
    def stop(self): self.running=False
    def send(self,message): self.results[message.get('message_id','')]=message
    def receive(self): return self.q.get_nowait() if not self.q.empty() else None
    def submit(self,message): mid=f'm{len(self.results)+1}'; self.q.put({'message_id':mid,'text':message}); return mid
    def get_result(self,message_id): return self.results.get(message_id,{})
