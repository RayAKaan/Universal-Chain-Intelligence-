from __future__ import annotations
import threading
from autonomy_system.communication.protocol_adapters.base_adapter import BaseAdapter
class CLIAdapter(BaseAdapter):
    name='cli'; protocol='cli'
    def __init__(self,hub=None): super().__init__(hub); self.thread=None
    def _loop(self):
        while self.running:
            try: txt=input('uci> ').strip()
            except EOFError: break
            if not txt: continue
            if self.hub: resp=self.hub.handle_message(self.hub.parser.parse(txt,'cli')); print(resp.content.get('result'))
            if txt=='shutdown': self.running=False
    def start(self): self.running=True; self.thread=threading.Thread(target=self._loop,daemon=True); self.thread.start()
    def stop(self): self.running=False
    def send(self,message): print(message)
    def receive(self): return None
