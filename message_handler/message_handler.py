import logging
import sqlite3
from typing import Tuple
import telegram

from telegram import Update
from telegram.ext import ContextTypes

from filters.question_filter import ContextSavingFilter, OpenAiQuestionFilter
from message_handler.message_types import RequestMessage
from repositories.user import get_user_from_db

filters = [ContextSavingFilter(OpenAiQuestionFilter())]

logger = logging.getLogger(__name__)

async def handle_incoming_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user = get_user_from_db(update.message.from_user.username)
    if user is None:
        logger.warning('User not found')
        await update.message.reply_text('YOU SHALL NOT PASS!')
        return
    logger.info(f'User found: {user.id}')
    rm = RequestMessage.from_telegram_message(update.message, user.id)
    for filter in filters:
        if filter.applies_to(rm):
            logger.info('Found applicable filter')
            try:
                ans = filter.process(rm)
                await update.message.reply_text(ans.text)
                return
            except Exception as e:
                print(f'Failed to process message: {e}')
                return
           
    await update.message.reply_text('Could not process your message.')

