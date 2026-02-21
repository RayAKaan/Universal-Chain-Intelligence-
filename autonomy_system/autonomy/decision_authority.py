from __future__ import annotations
from dataclasses import dataclass
from autonomy_system.models.autonomy_state import AutonomyLevel
@dataclass
class ApprovalResult: approved:bool; reason:str; approved_by:str
class DecisionAuthority:
    def decide(self,action,context,autonomy_level:AutonomyLevel,safety_report=None):
        if safety_report and not getattr(safety_report,'is_safe',True): return ApprovalResult(False,'safety governor rejection','safety_governor')
        if autonomy_level==AutonomyLevel.PASSIVE: return ApprovalResult(False,'human approval required','human')
        if autonomy_level==AutonomyLevel.SUPERVISED and action in {'execute_goal','acquire_capability','modify_self'}: return ApprovalResult(False,'approval required','human')
        return ApprovalResult(True,'auto-approved','auto')
