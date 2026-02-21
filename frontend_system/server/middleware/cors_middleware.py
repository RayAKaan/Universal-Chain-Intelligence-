
class CORSMiddleware:
    def __init__(self, config): self.config=config
    def headers(self):
        if not self.config.ENABLE_CORS: return {}
        return {
            'Access-Control-Allow-Origin': ','.join(self.config.CORS_ORIGINS),
            'Access-Control-Allow-Methods':'GET,POST,PUT,DELETE,OPTIONS',
            'Access-Control-Allow-Headers':'Content-Type,Authorization'
        }
