
from uuid import uuid4

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create(self, data=None):
        sid=str(uuid4()); self.sessions[sid]=data or {}; return sid
    def get(self,sid): return self.sessions.get(sid,{})
