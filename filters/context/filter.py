import logging
from typing import List
from filters.filter_types import Filter

from message_handler.message_types import RequestMessage, ResponseMessage
from repositories.app import AppRepository
from repositories.history import History, HistoryRepository

logger = logging.getLogger(__name__)

class ContextSavingFilter (Filter):
    def __init__(self, filters: List[Filter]):
        self.filters = filters
        self.history_repository = HistoryRepository()
        self.app_repository = AppRepository()

    def applies_to(self, msg: RequestMessage):
        return True

    def process(self, msg: RequestMessage):
        user_query = msg.text
    
        for filter in self.filters:
            if filter.applies_to(msg):
                response =  filter.process(msg)
                app_response = response.app_response if response.app_response is not None else response.text
                try:
                    app_id = self.app_repository.get_id_by_name(response.responding_application)  
                    self.history_repository.save(msg.user_id, History(user_query, app_response, app_id=app_id))
                    logger.info(f'Context saved for user {msg.user_id}')
                except Exception as e:
                    logger.error(f'Failed to save context for user {msg.user_id}: {e}')
                return response
        
        return ResponseMessage("I don't know how to answer that")