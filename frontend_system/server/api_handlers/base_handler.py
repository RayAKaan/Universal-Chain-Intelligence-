import json


class BaseHandler:
    def __init__(self, connector):
        self.uci = connector

    def response(self, data=None, error=None, status=200):
        return status, {"ok": error is None, "data": data, "error": error}

    def ok(self, data=None, status=200):
        return self.response(data=data, status=status)

    def fail(self, message, status=400):
        return self.response(error=message, status=status)


BaseAPIHandler = BaseHandler
