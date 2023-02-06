import logging
from typing import List
from filters.filter_types import Filter

from message_handler.message_types import RequestMessage, ResponseMessage
from repositories.history import QAPair, save_history_for_user

logger = logging.getLogger(__name__)

class ContextSavingFilter (Filter):
    def __init__(self, filters: List[Filter]):
        self.filters = filters

    def applies_to(self, msg: RequestMessage):
        return True

    def process(self, msg: RequestMessage):
        user_query = msg.text
    
        for filter in self.filters:
            if filter.applies_to(msg):
                response =  filter.process(msg)
                app_response = response.app_response if response.app_response is not None else response.text
                try:
                    save_history_for_user(msg.user_id, QAPair(user_query, app_response))
                    logger.info(f'Context saved for user {msg.user_id}')
                except Exception as e:
                    logger.error(f'Failed to save context for user {msg.user_id}: {e}')
                return response
        
        return ResponseMessage("I don't know how to answer that")