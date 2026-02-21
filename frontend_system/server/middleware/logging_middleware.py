
import logging
class LoggingMiddleware:
    def __init__(self,name='frontend.http'): self.log=logging.getLogger(name)
    def log_request(self, method, path, code): self.log.info('%s %s -> %s',method,path,code)
