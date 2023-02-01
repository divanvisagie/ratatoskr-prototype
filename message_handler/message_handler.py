from telegram import Update
from telegram.ext import ContextTypes
from abc import ABC, abstractmethod

from filters.question_filter import QuestionFilter
from message_handler.message_types import RequestMessage

filters = [QuestionFilter()]

async def handle_incoming_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    print('got message')
   
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

