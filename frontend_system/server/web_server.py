
from __future__ import annotations
import json, gzip
from io import BytesIO
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from threading import Thread
from urllib.parse import urlparse

from frontend_system.server.api_router import APIRouter
from frontend_system.server.static_handler import StaticHandler
from frontend_system.server.middleware.auth_middleware import AuthMiddleware
from frontend_system.server.middleware.cors_middleware import CORSMiddleware
from frontend_system.server.middleware.logging_middleware import LoggingMiddleware
from frontend_system.server.middleware.safety_middleware import SafetyMiddleware

class UCIWebServer:
    def __init__(self, host='0.0.0.0', port=8080, uci_connector=None, config=None):
        self.host=host; self.port=port; self.uci=uci_connector; self.config=config; self.httpd=None; self.thread=None

    def start(self):
        router=APIRouter(self.uci); static=StaticHandler(self.config.STATIC_DIRECTORY,self.config.TEMPLATE_DIRECTORY)
        auth=AuthMiddleware(self.config); cors=CORSMiddleware(self.config); log=LoggingMiddleware(); safe=SafetyMiddleware()

        class Handler(BaseHTTPRequestHandler):
            server_version='UCIFrontend/1.0'
            def _body(self):
                l=int(self.headers.get('Content-Length',0));
                if l<=0:return {}
                try:return json.loads(self.rfile.read(l).decode())
                except Exception:return {}
            def _write(self,code,body:bytes,ctype='application/json',cache=True):
                accept=self.headers.get('Accept-Encoding','')
                compressed=False
                if self.server.compress and ('gzip' in accept) and ctype.startswith(('text/','application/json','application/javascript')):
                    buf=BytesIO();
                    with gzip.GzipFile(fileobj=buf,mode='wb') as f: f.write(body)
                    body=buf.getvalue(); compressed=True
                self.send_response(code)
                self.send_header('Content-Type',ctype)
                self.send_header('Content-Length',str(len(body)))
                if compressed:self.send_header('Content-Encoding','gzip')
                if cache:self.send_header('Cache-Control',f'public, max-age={self.server.cache_age}')
                else:self.send_header('Cache-Control','no-store')
                for k,v in cors.headers().items(): self.send_header(k,v)
                self.end_headers(); self.wfile.write(body); log.log_request(self.command,self.path,code)
            def do_OPTIONS(self): self._write(200,b'',ctype='text/plain',cache=False)
            def do_GET(self):
                p=urlparse(self.path).path
                if p.startswith('/api/'):
                    return self._api()
                if p=='/ws':
                    return self._write(200,json.dumps({'events':[]}).encode(),cache=False)
                fp=static.resolve(p)
                if fp and fp.exists():
                    data,ctype=static.read(fp)
                    return self._write(200,data,ctype,cache=('/static/' in p))
                return self._write(404,b'not found',ctype='text/plain',cache=False)
            def do_POST(self):
                if self.path.startswith('/api/'): return self._api()
                return self._write(404,b'not found',ctype='text/plain',cache=False)
            def _api(self):
                ok,msg=auth.check(self.headers,self.path)
                if not ok:return self._write(401,json.dumps({'error':msg}).encode(),cache=False)
                payload=self._body() if self.command in ('POST','PUT','DELETE') else {}
                allowed,why=safe.check(self.path,payload)
                if not allowed:return self._write(403,json.dumps({'error':why}).encode(),cache=False)
                code,data=router.route(self.command,self.path,payload)
                return self._write(code,json.dumps(data,default=str).encode(),cache=False)

        self.httpd=ThreadingHTTPServer((self.host,self.port),Handler)
        self.httpd.compress=bool(getattr(self.config,'COMPRESS_TEXT_RESPONSES',True))
        self.httpd.cache_age=int(getattr(self.config,'STATIC_CACHE_MAX_AGE',3600))
        self.thread=Thread(target=self.httpd.serve_forever,daemon=True)
        self.thread.start()

    def stop(self):
        if self.httpd:
            self.httpd.shutdown(); self.httpd.server_close()
