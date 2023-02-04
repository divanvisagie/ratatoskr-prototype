import logging

from telegram import Update
from telegram.ext import ContextTypes
from filters.code_question_filter import OpenAiCodeGenFilter
from filters.context_saving_filter import ContextSavingFilter
from filters.notion_filter import NotionFilter

from filters.question_filter import OpenAiQuestionFilter
from message_handler.message_types import RequestMessage
from repositories.user import get_user_from_db

filters = [ContextSavingFilter([
    NotionFilter(),
    OpenAiQuestionFilter([OpenAiCodeGenFilter()])
])]

logger = logging.getLogger(__name__)

async def handle_incoming_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    if update.message.reply_to_message is not None:
        logger.info("We have received a reply")
        await update.message.reply_text('We do not support replies yet')
        return

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
                await update.message.reply_text(text=ans.text, parse_mode='Markdown')
                return
            except Exception as e:
                print(f'Failed to process message: {e}')
                return
           
    await update.message.reply_text('Could not process your message.')

