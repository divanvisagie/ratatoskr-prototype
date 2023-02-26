import logging
from typing import List
from filters.filter_types import Filter

from message_handler.message_types import RequestMessage, ResponseMessage
from repositories.app import AppRepository
from repositories.history import NewHistory, HistoryRepository

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
        logger.info(f'{self.__class__.__name__} Processing message: {user_query}')
        for filter in self.filters:
            logger.info(f'Checking if filter {filter.__class__.__name__} applies')
            if filter.applies_to(msg):
                logger.info(f'Applying filter {filter.__class__.__name__}')
                response =  filter.process(msg)
                app_response = response.app_response if response.app_response is not None else response.text
                try: 
                    self.history_repository.save(msg.user_id, NewHistory(user_query, app_response, response.responding_application))
                    logger.info(f'Context saved for user {msg.user_id}')
                except Exception as e:
                    logger.error(f'Failed to save context for user {msg.user_id}: {e}')
                return response
        
        return ResponseMessage("I don't know how to answer that")