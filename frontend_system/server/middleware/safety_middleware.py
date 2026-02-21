
class SafetyMiddleware:
    def check(self, path, payload):
        text=str(payload).lower()
        if 'disable safety' in text or 'bypass' in text:
            return False, 'Safety middleware blocked request content'
        return True, ''
