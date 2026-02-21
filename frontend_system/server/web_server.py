
from __future__ import annotations
import json
import logging
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

from frontend_system.server.api_router import APIRouter
from frontend_system.server.static_handler import StaticHandler
from frontend_system.server.middleware.auth_middleware import AuthMiddleware
from frontend_system.server.middleware.cors_middleware import CORSMiddleware
from frontend_system.server.middleware.logging_middleware import LoggingMiddleware
from frontend_system.server.middleware.safety_middleware import SafetyMiddleware

class UCIWebServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 8080, uci_connector=None, config=None):
        self.host=host; self.port=port; self.uci=uci_connector; self.config=config
        self._httpd=None; self._thread=None

    def start(self)->None:
        router=APIRouter(self.uci)
        static=StaticHandler(self.config.STATIC_DIRECTORY, self.config.TEMPLATE_DIRECTORY)
        auth=AuthMiddleware(self.config); cors=CORSMiddleware(self.config); logmw=LoggingMiddleware(); safemw=SafetyMiddleware()

        class Handler(BaseHTTPRequestHandler):
            def _send(self,code,body,btype='application/json'):
                self.send_response(code)
                self.send_header('Content-Type',btype)
                for k,v in cors.headers().items(): self.send_header(k,v)
                self.end_headers()
                self.wfile.write(body)
                logmw.log_request(self.command,self.path,code)

            def do_OPTIONS(self): self._send(200,b'')
            def _read_json(self):
                l=int(self.headers.get('Content-Length',0));
                if l<=0:return {}
                try:return json.loads(self.rfile.read(l).decode('utf-8'))
                except Exception:return {}

            def _handle_api(self):
                ok,msg=auth.check(self.headers,self.path)
                if not ok:return self._send(401,json.dumps({'error':msg}).encode())
                payload=self._read_json() if self.command in ('POST','PUT','DELETE') else {}
                safe,smsg=safemw.check(self.path,payload)
                if not safe:return self._send(403,json.dumps({'error':smsg}).encode())
                code,data=router.route(self.command,self.path,payload)
                self._send(code,json.dumps(data,default=str).encode())

            def do_GET(self):
                p=urlparse(self.path).path
                if p.startswith('/api/'): return self._handle_api()
                if p=='/ws':
                    return self._send(200,json.dumps({'events':[]}).encode())
                file_path=static.resolve(p)
                if file_path and file_path.exists():
                    data,ctype=static.read(file_path); return self._send(200,data,ctype)
                self._send(404,b'Not found','text/plain')

            def do_POST(self):
                if self.path.startswith('/api/'): return self._handle_api()
                self._send(404,b'Not found','text/plain')

        self._httpd=ThreadingHTTPServer((self.host,self.port),Handler)
        self._thread=threading.Thread(target=self._httpd.serve_forever,daemon=True)
        self._thread.start()

    def stop(self)->None:
        if self._httpd:
            self._httpd.shutdown(); self._httpd.server_close()
