import logging

from telegram import Update
from telegram.ext import ContextTypes
from capability.context.capability import ContextSavingFilter
from capability.duck_duck_go.capability import DuckDuckGoCapability
from capability.notion.capability import NotionCapability

from capability.chat_gpt.capability import ChatGptCapability
from capability.smart_switch.capability import SmartSwitchFilter
from message_handler.message_types import RequestMessage
from repositories.user import UserRepository

filters = [ContextSavingFilter([
    NotionCapability(),
    DuckDuckGoCapability(),
    SmartSwitchFilter(),
    ChatGptCapability([])
])]

logger = logging.getLogger(__name__)

async def handle_incoming_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Recieved message in context: {context}")
    """Echo the user message."""
    if update.message.reply_to_message is not None:
        logger.info("We have received a reply")
        await update.message.reply_text('We do not support replies yet')
        return

    user_repo = UserRepository()
    user =  user_repo.get_by_telegram_username(update.message.from_user.username)
    if user is None:
        logger.warning(f'User not found "{update.message.from_user.username}"')
        await update.message.reply_text('YOU SHALL NOT PASS!')
        return

    logger.info(f'User found: {user.id}')
    rm = RequestMessage.from_telegram_message(update.message, user.id)
    for filter in filters:
        if filter.relevance_to(rm):
            logger.info(f'Filter {filter.__class__.__name__} applies to message')
            try:
                ans = filter.apply(rm)
                await update.message.reply_text(text=ans.text, parse_mode='Markdown')
                return
            except Exception as e:
                print(f'Failed to process message: {e}')
                await update.message.reply_text('Something went wrong. I could not find a good reply.')
                return
           
    await update.message.reply_text('Could not process your message.')

