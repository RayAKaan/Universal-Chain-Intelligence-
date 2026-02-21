
class BaseAPIHandler:
    def __init__(self, connector):
        self.uci = connector

    @staticmethod
    def ok(data):
        return 200, data

    @staticmethod
    def error(msg, code=400):
        return code, {'error': msg}
