
from filters.filter_types import Capability, find_most_applicable
from message_handler.message_types import RequestMessage, ResponseMessage


class MockFilter(Capability):
    def __init__(self, application: float):
        self.application = application

    def relevance_to(self, msg: RequestMessage) -> float:
        return self.application
    
    def apply(self, msg: RequestMessage) -> ResponseMessage:
        return ResponseMessage('Filter1')

def applicability_case(filters, expected_filter, expected_confidence):
    m = RequestMessage('mock message', 'mock user')
    actual_filter, actual_confidence = find_most_applicable(filters, m)
    assert actual_filter == expected_filter
    assert actual_confidence == expected_confidence

def test_find_most_applicable():
    highest = MockFilter(0.9)
    # Test cases where order is different to ensure we aren't picking by order
    applicability_case([highest, MockFilter(0.8), MockFilter(0.5)], highest, 0.9)
    applicability_case([MockFilter(0.8), highest, MockFilter(0.5)], highest, 0.9)
    applicability_case([MockFilter(0.8), MockFilter(0.5), highest], highest, 0.9)