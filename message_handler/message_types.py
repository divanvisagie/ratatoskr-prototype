import telegram
from opentelemetry.trace import Tracer, Span


class RequestMessage(object):
    """Represents a user input message"""
    def __init__(self, text: str, user_id: int, tracer: Tracer = None, parent_span: Span = None):
        self.text = text
        self.user_id = user_id
        self.tracer = tracer
        self.parent_span = parent_span

    def __str__(self):
        return f'RequestMessage: {self.text}'
    
    @classmethod
    def from_telegram_message(cls, msg: telegram.Message, userId: int, tracer: Tracer = None, parent_span: Span = None):
        return cls(msg.text, userId, tracer, parent_span)


class ResponseMessage(object):
    """Represents a response to a user input message"""
    def __init__(self, text: str, responding_application: str = None, app_response: str = None):
        self.text = text
        self.responding_application = responding_application
        self.app_response = app_response

    def __str__(self):
        return f'ResponseMessage: {self.text}'