from telegram import Update
from telegram.ext import ContextTypes
from abc import ABC, abstractmethod

from .message_types import RequestMessage

class Filter (ABC):
    """Represents a filter that can be applied to a message"""
    @abstractmethod
    def applies_to(self, msg: RequestMessage):
        pass
    
    @abstractmethod
    def process(self, msg: RequestMessage):
        pass


class QuestionFilter (Filter):
    def applies_to(self, msg: RequestMessage):
        return True

    def process(self, msg: RequestMessage):
        return 'I am the captain now'


async def handle_incoming_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    print('got message')
    filters = [QuestionFilter()]
    rm = RequestMessage.from_telegram_message(update.message)
    for filter in filters:
        if filter.applies_to(rm):
            print('Found applicable filter')
            try:
                ans = filter.process(rm)
                await update.message.reply_text(ans)
                return
            except Exception as e:
                print(e)
                print('Failed to create RequestMessage')
                return
           
    await update.message.reply_text('Could not process your message.')

