from __future__ import annotations
import json, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from autonomy_system.communication.protocol_adapters.base_adapter import BaseAdapter
class HTTPAdapter(BaseAdapter):
    name='http'; protocol='http'
    def __init__(self,hub=None,port=8080): super().__init__(hub); self.port=port; self.server=None; self.thread=None
    def start(self):
        hub=self.hub
        class H(BaseHTTPRequestHandler):
            def _send(self,obj,code=200): self.send_response(code); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(json.dumps(obj,default=str).encode())
            def do_GET(self):
                if self.path.startswith('/status'): self._send({'status':'ok'})
                elif self.path.startswith('/capabilities'): self._send({'capabilities':[]})
                else: self._send({'error':'not found'},404)
            def do_POST(self):
                n=int(self.headers.get('Content-Length','0')); body=self.rfile.read(n).decode() if n else ''
                if self.path.startswith('/goals') and hub:
                    resp=hub.handle_message(hub.parser.parse(body or '','http')); self._send(resp.content)
                else: self._send({'ok':True})
            def log_message(self,*a): return
        self.server=HTTPServer(('0.0.0.0',self.port),H); self.running=True; self.thread=threading.Thread(target=self.server.serve_forever,daemon=True); self.thread.start()
    def stop(self): self.running=False; self.server and self.server.shutdown()
    def send(self,message): pass
    def receive(self): return None
