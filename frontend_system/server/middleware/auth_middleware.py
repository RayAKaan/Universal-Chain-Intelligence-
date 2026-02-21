
class AuthMiddleware:
    def __init__(self, config): self.config=config
    def check(self, headers, path):
        if not self.config.AUTH_ENABLED: return True, ''
        if path.endswith('/panic') or path.endswith('/reset') or path.endswith('/shutdown'):
            token=headers.get('Authorization','').replace('Bearer ','')
            return token==self.config.AUTH_TOKEN, 'unauthorized'
        return True,''
