from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
class MessageType(str,Enum): GOAL_REQUEST='GOAL_REQUEST'; STATUS_QUERY='STATUS_QUERY'; CAPABILITY_QUERY='CAPABILITY_QUERY'; ADMIN_COMMAND='ADMIN_COMMAND'; GOAL_RESULT='GOAL_RESULT'; STATUS_RESPONSE='STATUS_RESPONSE'; ERROR_RESPONSE='ERROR_RESPONSE'; NOTIFICATION='NOTIFICATION'; HEARTBEAT='HEARTBEAT'
@dataclass
class CommunicationMessage:
    direction:str; protocol:str; message_type:MessageType; content:dict
    message_id:str=field(default_factory=lambda:str(uuid4())); sender:str=''; receiver:str=''; correlation_id:str=''; timestamp:datetime=field(default_factory=lambda:datetime.now(timezone.utc)); metadata:dict=field(default_factory=dict)
