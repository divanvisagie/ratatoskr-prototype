import telegram

class RequestMessage(object):
    """Represents a user input message"""
    def __init__(self, text: str, id: int):
        self.text = text
        self.user_id = id

    def __str__(self):
        return f'RequestMessage: {self.text}'
    
    @classmethod
    def from_telegram_message(cls, msg: telegram.Message, userId: int):
        return cls(msg.text, userId)


class ResponseMessage(object):
    """Represents a response to a user input message"""
    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return f'ResponseMessage: {self.text}'