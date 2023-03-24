import logging
from typing import List
from capability.capability import Capability, RelevanceRequest
from log_factory.logger import create_logger

from message_handler.message_types import RequestMessage, ResponseMessage
from repositories.history import NewHistory, HistoryRepository

logger = create_logger(__name__)

class ContextSavingLayer (Capability):
    def __init__(self, filters: List[Capability]):
        super().__init__()
        self.capabilities = filters
        self.history_repository = HistoryRepository()

    def relevance_to(self, msg: RequestMessage):
        return True

    def apply(self, msg: RequestMessage):
        user_query = msg.text
        logger.info(f'{self.__class__.__name__} Processing message: {user_query}')
        for capability in self.capabilities:
            logger.info(f'Checking if filter {capability.__class__.__name__} applies')
            if capability.ask(RelevanceRequest(msg)):
                logger.info(f'Applying filter {capability.__class__.__name__}')
                response =  capability.ask(msg)
                app_response = response.app_response if response.app_response is not None else response.text
                try: 
                    self.history_repository.save(NewHistory(msg.user_id, question=user_query, answer=app_response, responder=response.responding_application))
                    logger.info(f'Context saved for user {msg.user_id}')
                except Exception as e:
                    logger.error(f'Failed to save context for user {msg.user_id}: {e}')
                return response
        
        return ResponseMessage("I don't know how to answer that")