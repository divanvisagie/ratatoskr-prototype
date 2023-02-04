import logging
from clients.notion_client import add_entry_to_todays_page
from filters.filter_types import Filter
from message_handler.message_types import RequestMessage, ResponseMessage

logger = logging.getLogger(__name__)

class NotionFilter (Filter):
    def __init__(self, filter: Filter):
        self.filter = filter

    def applies_to(self, msg: RequestMessage):
        return False

    def process(self, msg: RequestMessage):
        logger.info(f'Context saved for user {msg.user_id}')
        add_entry_to_todays_page(msg.text)
        return ResponseMessage("I shall write this in runes Havi")