from __future__ import annotations
class HumanInLoop:
    def request_input(self,prompt,timeout_seconds=None): return None
    def notify(self,message,severity='info'): print(f'[NOTIFY:{severity}] {message}')
    def request_approval(self,action,details,timeout_seconds=300): return False
    def is_human_available(self): return False
