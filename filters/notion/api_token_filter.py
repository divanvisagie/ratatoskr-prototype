import logging
from typing import Callable
import spacy

from filters.filter_types import Filter
from message_handler.message_types import RequestMessage, ResponseMessage
from repositories.history import get_app_id_by_name, get_last_answer
from repositories.secrets import Secret, get_app_secret_for_user, save_secret

logger = logging.getLogger(__name__)
nlp = spacy.load("en_core_web_sm")

class MissingTokenFilter (Filter):

    def __init__(self, app_id: int, api_token_key: str, request_message: str, extract: Callable[[str], str]):
        """Filter that asks for a token if the user has not yet provided one."""
        self.app_id = app_id
        self.api_token_key = api_token_key
        self.extract = extract
        self.request_message = request_message

    def applies_to(self, msg: RequestMessage):
        """Applies if the user has not yet provided token or if the message contains a token."""
        token = get_app_secret_for_user(msg.user_id, self.app_id, self.api_token_key)

        if token is None:
            return True

        last_answer = get_last_answer(msg.user_id)
        if last_answer == self.api_token_key and self.extract(msg.text) is not None:
            return True

    def process(self, msg: RequestMessage) -> ResponseMessage:
        if get_app_secret_for_user(msg.user_id, self.app_id, self.api_token_key) is None:
            token = self.extract(msg.text)
            if token is None:
                return ResponseMessage(
                    self.request_message, 
                    "Notion", 
                    self.api_token_key
                )
            save_secret(Secret(msg.user_id, self.app_id, self.api_token_key, token))
            return ResponseMessage("I found a token in your message. I will use it to save messages in Notion for you.")