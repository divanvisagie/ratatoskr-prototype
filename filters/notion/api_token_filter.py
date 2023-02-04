import logging
import spacy

from filters.filter_types import Filter
from message_handler.message_types import RequestMessage, ResponseMessage
from repositories.history import get_last_answer
from repositories.secrets import Secret, get_app_secret_for_user, save_secret

TOKEN_REQUEST_MESSAGE = """
I can save messages in Notion if you give me a token.
You can create the token by:

- Going to https://www.notion.so/my-integrations.
- Clicking on the 'Create new Integration' button.
- Giving it it a name and selecting 'Internal Integration'.
- Then clicking on 'Submit'.

You can then copy the token and send it to me.
"""
API_TOKEN_REQUEST = "API_TOKEN_REQUEST"

logger = logging.getLogger(__name__)
nlp = spacy.load("en_core_web_sm")

def extract_token_from_message(msg: str) -> str:
    doc = nlp(msg)
    for token in doc:
        if token.text.startswith('secret_'):
            return token.text
    return None

class ApiTokenFilter (Filter):

    def applies_to(self, msg: RequestMessage):
        last_answer = get_last_answer(msg.user_id)
        if last_answer == API_TOKEN_REQUEST and extract_token_from_message(msg.text) is not None:
            return True

    def process(self, msg: RequestMessage) -> ResponseMessage:
        if get_app_secret_for_user(msg.user_id, self.app_id, API_TOKEN_REQUEST) is None:
            token = extract_token_from_message(msg.text)
            if token is None:
                return ResponseMessage(
                    TOKEN_REQUEST_MESSAGE, 
                    "Notion", 
                    API_TOKEN_REQUEST
                )
            save_secret(Secret(msg.user_id, self.app_id, API_TOKEN_REQUEST, token))
            return ResponseMessage("I found a token in your message. I will use it to save messages in Notion for you.")