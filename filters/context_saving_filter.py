import logging
from filters.filter_types import Filter

from message_handler.message_types import RequestMessage
from repositories.history import QAPair, save_history_for_user

logger = logging.getLogger(__name__)

class ContextSavingFilter (Filter):
    def __init__(self, filter: Filter):
        self.filter = filter

    def applies_to(self, msg: RequestMessage):
        return True

    def process(self, msg: RequestMessage):
        response = self.filter.process(msg)
        save_history_for_user(msg.user_id, QAPair(msg.text, response.text))
        logger.info(f'Context saved for user {msg.user_id}')
        return response