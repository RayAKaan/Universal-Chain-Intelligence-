from __future__ import annotations
from autonomy_system.models.autonomy_state import AutonomyLevel, AutonomyPermissions
PASSIVE_PERMISSIONS=AutonomyPermissions(False,False,False,False,False,False,False,False,1,50.0,['all'])
SUPERVISED_PERMISSIONS=AutonomyPermissions(True,False,False,False,False,False,False,True,3,60.0,['execute_goal','acquire_capability','modify_self'])
GUIDED_PERMISSIONS=AutonomyPermissions(True,True,False,True,False,False,True,True,5,75.0,['modify_self','prune_capability','replace_strategy'])
AUTONOMOUS_PERMISSIONS=AutonomyPermissions(True,True,True,True,True,True,True,True,10,85.0,['architecture_change'])
FULL_AUTONOMY_PERMISSIONS=AutonomyPermissions(True,True,True,True,True,True,True,True,20,90.0,[])
LEVEL_PERMISSIONS={AutonomyLevel.PASSIVE:PASSIVE_PERMISSIONS,AutonomyLevel.SUPERVISED:SUPERVISED_PERMISSIONS,AutonomyLevel.GUIDED:GUIDED_PERMISSIONS,AutonomyLevel.AUTONOMOUS:AUTONOMOUS_PERMISSIONS,AutonomyLevel.FULL_AUTONOMY:FULL_AUTONOMY_PERMISSIONS}
