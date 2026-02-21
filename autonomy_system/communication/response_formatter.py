from __future__ import annotations
import json
class ResponseFormatter:
    def format_goal_result(self,goal_record): return f"Goal {goal_record.record_id}: {goal_record.status.value}"
    def format_status(self,status): return json.dumps(status,default=str,indent=2) if not isinstance(status,str) else status
    def format_error(self,error): return f'ERROR: {error}'
    def format_capabilities(self,capabilities): return '\n'.join(str(c) for c in capabilities)
    def format_response(self,result,message_type,protocol):
        if protocol=='http': return json.dumps(result,default=str)
        return str(result)
