from abc import ABC, abstractmethod

from message_handler.message_types import RequestMessage, ResponseMessage


class Filter (ABC):
  
    @abstractmethod
    def applies_to(self, msg: RequestMessage):
        """Represents a filter that can be applied to a message"""
        pass
    
    @abstractmethod
    def process(self, msg: RequestMessage) -> ResponseMessage:
        """Defines the logic to process the message"""
        pass
