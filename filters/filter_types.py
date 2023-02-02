from abc import ABC, abstractmethod

from message_handler.message_types import RequestMessage, ResponseMessage


class Filter (ABC):
    """Represents a filter that can be applied to a message"""
    @abstractmethod
    def applies_to(self, msg: RequestMessage):
        pass
    
    @abstractmethod
    def process(self, msg: RequestMessage) -> ResponseMessage:
        pass
