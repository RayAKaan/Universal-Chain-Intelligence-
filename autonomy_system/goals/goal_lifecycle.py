from __future__ import annotations
from autonomy_system.models.goal_record import GoalRecordStatus
TRANSITIONS={GoalRecordStatus.RECEIVED:[GoalRecordStatus.QUEUED],GoalRecordStatus.QUEUED:[GoalRecordStatus.INTERPRETING,GoalRecordStatus.DEFERRED],GoalRecordStatus.INTERPRETING:[GoalRecordStatus.PLANNING],GoalRecordStatus.PLANNING:[GoalRecordStatus.EXECUTING],GoalRecordStatus.EXECUTING:[GoalRecordStatus.COMPLETED,GoalRecordStatus.FAILED,GoalRecordStatus.PAUSED],GoalRecordStatus.PAUSED:[GoalRecordStatus.EXECUTING],GoalRecordStatus.DEFERRED:[GoalRecordStatus.QUEUED]}
class GoalLifecycle:
    def transition(self,record,new_status):
        if new_status in TRANSITIONS.get(record.status,[]) or new_status==GoalRecordStatus.CANCELLED: record.status=new_status; return True
        return False
    def get_valid_transitions(self,current): return TRANSITIONS.get(current,[])
