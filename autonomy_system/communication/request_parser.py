from __future__ import annotations
from autonomy_system.models.communication_message import CommunicationMessage, MessageType
class RequestParser:
    def parse(self,raw_input,protocol):
        txt=(raw_input or '').strip(); low=txt.lower()
        if low.startswith('status') or 'how are you' in low: t=MessageType.STATUS_QUERY
        elif low.startswith('capabilities') or 'what can you' in low: t=MessageType.CAPABILITY_QUERY
        elif low.startswith('admin:') or low.startswith('config:'): t=MessageType.ADMIN_COMMAND
        else: t=MessageType.GOAL_REQUEST
        return CommunicationMessage(direction='inbound',protocol=protocol,message_type=t,content={'text':txt})
