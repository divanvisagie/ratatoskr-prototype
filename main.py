from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from os import environ
import logging

from message_handler.message_handler import handle_incoming_telegram_message

TELEGRAM_BOT_TOKEN = environ['TELEGRAM_BOT_TOKEN']

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Pong {update.effective_user.first_name}')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = create_logger__name__)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler('ping', ping))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_incoming_telegram_message))
    logger.info('starting app..')
    app.run_polling()

if __name__ == "__main__":
    main()
