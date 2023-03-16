from abc import ABC, abstractmethod
from typing import List, Tuple

from message_handler.message_types import RequestMessage, ResponseMessage

class Capability (ABC):
    """Defines the interface for a Capability"""
    description = "Not Implemented" # If not implemented then will be ignored by fallback mechanism
    
    def relevance_to(self, msg: RequestMessage) -> float:
        """Checks how relevant the capability is to the message"""
        return 0.00
    
    @abstractmethod
    def apply(self, msg: RequestMessage) -> ResponseMessage:
        """Defines the logic to process the message"""
        pass


def find_most_applicable(filters: List[Capability], message: RequestMessage) -> Tuple[Capability, float]:
    """
    Finds the most applicable filter in a list of filters

    Args:
        filters (List[Filter]): The list of filters to search
        message (RequestMessage): The message to search for

    Returns:
        Tuple[Filter, float]: The most applicable filter and the confidence of the filter's applicability
    """
    current_best = None
    current_best_relevance = 0.0
    for filter in filters:
        if current_best is None:
            current_best = filter
            current_best_relevance = filter.relevance_to(message)
        else:
            relevance = filter.relevance_to(message)
            if relevance > current_best_relevance:
                current_best = filter
                current_best_relevance = relevance

    return (current_best, current_best_relevance)

