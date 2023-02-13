from abc import ABC, abstractmethod

from message_handler.message_types import RequestMessage, ResponseMessage


class Repository (ABC):

    @abstractmethod
    def get_by_id(self, id):
        """Get the item by Id"""
        pass

    @abstractmethod
    def save(self, id, item):
        """Save the item"""
        pass