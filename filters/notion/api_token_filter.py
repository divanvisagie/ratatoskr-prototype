import logging
from typing import Callable
import spacy

from filters.filter_types import Capability
from message_handler.message_types import RequestMessage, ResponseMessage
from repositories.history import HistoryRepository
from repositories.secret import Secret, SecretRepository

logger = logging.getLogger(__name__)
nlp = spacy.load("en_core_web_sm")

class MissingTokenFilter (Capability):

    def __init__(self, api_token_key: str, request_message: str, extract: Callable[[str], str]):
        """Filter that asks for a token if the user has not yet provided one."""
        self.api_token_key = api_token_key
        self.extract = extract
        self.request_message = request_message
        self.history_repository = HistoryRepository()
        self.secret_repository = SecretRepository()

    def relevance_to(self, msg: RequestMessage):
        """Applies if the user has not yet provided token or if the message contains a token."""
        last_answer = self.history_repository.get_by_id(msg.user_id,1)[0].answer
        if last_answer == self.api_token_key and self.extract(msg.text) is not None:
            return True

    def apply(self, msg: RequestMessage) -> ResponseMessage:
        if self.secret_repository.get_app_secret_for_user(msg.user_id, self.app_id, self.api_token_key) is None:
            token = self.extract(msg.text)
            if token is None:
                return ResponseMessage(
                    self.request_message, 
                    "Notion", 
                    self.api_token_key
                )
            self.secret_repository.save_secret(Secret(msg.user_id, self.app_id, self.api_token_key, token))
            return ResponseMessage("I found a token in your message. I will use it to save messages in Notion for you.")