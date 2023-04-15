from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from os import environ
import logging
from log_factory.logger import create_logger

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

from message_handler.message_handler import TelegramMessageHandler

TELEGRAM_BOT_TOKEN = environ['TELEGRAM_BOT_TOKEN']

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Pong {update.effective_user.first_name}')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = create_logger(__name__)


#Enable tracing
resource = Resource({ SERVICE_NAME: "muninn"})
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

def main():
    telegram_message_handler = TelegramMessageHandler(tracer)

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler('ping', ping))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_message_handler.handle_incoming_telegram_message))
    logger.info('starting app..')
    app.run_polling()

if __name__ == "__main__":
    main()
