import telegram

class RequestMessage(object):
    """Represents a user input message"""
    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return f'RequestMessage: {self.text}'
    
    @classmethod
    def from_telegram_message(cls, msg: telegram.Message):
        return cls(msg.text)