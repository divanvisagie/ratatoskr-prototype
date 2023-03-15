from abc import ABC, abstractmethod
from typing import List, Tuple

from message_handler.message_types import RequestMessage, ResponseMessage

class Filter (ABC):
    """Defines the interface for a filter"""
    description = "Not Implemented" # If not implemented then will be ignored by fallback mechanism
    
    def applies_to(self, msg: RequestMessage) -> float:
        """Represents a filter that can be applied to a message"""
        return 0.00
    
    @abstractmethod
    def process(self, msg: RequestMessage) -> ResponseMessage:
        """Defines the logic to process the message"""
        pass


def find_most_applicable(filters: List[Filter], message: RequestMessage) -> Tuple[Filter, float]:
    """
    Finds the most applicable filter in a list of filters

    Args:
        filters (List[Filter]): The list of filters to search
        message (RequestMessage): The message to search for

    Returns:
        Tuple[Filter, float]: The most applicable filter and the confidence of the filter's applicability
    """
    current_best = None
    current_best_applicability = 0.0
    for filter in filters:
        if current_best is None:
            current_best = filter
            current_best_applicability = filter.applies_to(message)
        else:
            applicability = filter.applies_to(message)
            if applicability > current_best_applicability:
                current_best = filter
                current_best_applicability = applicability

    return (current_best, current_best_applicability)

