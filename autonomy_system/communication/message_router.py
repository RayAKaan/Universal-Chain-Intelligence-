from __future__ import annotations
from autonomy_system.models.communication_message import CommunicationMessage, MessageType
class MessageRouter:
    def __init__(self): self.handlers={}
    def register_handler(self,message_type,handler): self.handlers[message_type]=handler
    def route(self,message):
        h=self.handlers.get(message.message_type)
        if h: out=h(message)
        else: out={'error':'no handler'}
        return CommunicationMessage(direction='outbound',protocol=message.protocol,message_type=MessageType.STATUS_RESPONSE if message.message_type==MessageType.STATUS_QUERY else MessageType.GOAL_RESULT,content={'result':out},correlation_id=message.message_id)
