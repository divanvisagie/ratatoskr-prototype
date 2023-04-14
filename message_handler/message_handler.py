from telegram import Update
from telegram.ext import ContextTypes
from capability.capability import Capability
from capability.context.capability import ContextSavingLayer
from capability.duck_duck_go.capability import DuckDuckGoCapability
from capability.notion.capability import NotionCapability

from capability.chat_gpt.capability import ChatGptCapability
from capability.smart_switch.capability import SmartSwitchFilter
from log_factory.logger import create_logger
from message_handler.message_types import RequestMessage
from repositories.user import UserRepository

from opentelemetry.trace import Tracer

notion_capability = NotionCapability()
duck_duck_go_capability = DuckDuckGoCapability()
smart_switch_filter = SmartSwitchFilter()
chat_gpt_capability = ChatGptCapability([])
context_saving_layer = ContextSavingLayer([notion_capability, duck_duck_go_capability, smart_switch_filter, chat_gpt_capability])

logger = create_logger(__name__)

user_repo = UserRepository()

class TelegramMessageHandler:
    def __init__(self, tracer: Tracer):
        self.tracer = tracer

    async def handle_incoming_telegram_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        with self.tracer.start_as_current_span(f'TelegramMessageHandler.handle_incoming_telegram_message') as span:
            logger.info(f"Recieved message in context: {context}")
            """Echo the user message."""
            if update.message.reply_to_message is not None:
                logger.info("We have received a reply")
                await update.message.reply_text('We do not support replies yet')
                return

            user = user_repo.get_by_telegram_username(update.message.from_user.username)
            if user is None:
                logger.warning(f'User not found "{update.message.from_user.username}"')
                await update.message.reply_text('YOU SHALL NOT PASS!')
                return

            logger.info(f'User found: {user.id}')
            request_message = RequestMessage.from_telegram_message(update.message, user.id, self.tracer)
        
            if context_saving_layer.relevance_to(request_message):
                logger.info(f'Filter {context_saving_layer.__class__.__name__} applies to message')
                try:
                    await handle_message_with_capability(update, request_message, context_saving_layer)
                    return
                except Exception as e:
                    print(f'Failed to process message: {e}')
                    await update.message.reply_text('Something went wrong. I could not find a good reply.')
                    return
                
            await update.message.reply_text('Could not process your message.')

async def handle_message_with_capability(update: Update, req: RequestMessage, capability: Capability):
    ans = capability.apply(req)
    await update.message.reply_text(text=ans.text, parse_mode='Markdown')
