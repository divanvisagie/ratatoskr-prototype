import logging
import spacy

from clients.notion_client import add_entry_to_todays_page
from filters.filter_types import Filter
from message_handler.message_types import RequestMessage, ResponseMessage
from repositories.history import get_app_id_by_name, get_last_answer
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
TOKEN_SECRET_QUESTION = "Notion API Token"

logger = logging.getLogger(__name__)
nlp = spacy.load("en_core_web_sm")

def user_has_token(user_id: int, app_id: int) -> bool:
    secret = get_app_secret_for_user(user_id, app_id, TOKEN_SECRET_QUESTION)
    if secret is not None:
        return True
    return False

def get_token(msg: str) -> str:
    doc = nlp(msg)
    for token in doc:
        if token.text.startswith('secret_'):
            return token.text
    return None

def save_requested(question: str) -> bool:
    doc = nlp(question)
    for token in doc:
        if token.head.pos_ == "VERB" and token.head.text.lower() in ["save", "store", "remember", "keep"]:
            return True
    return False


class NotionFilter (Filter):
    def __init__(self):
        self.app_id = get_app_id_by_name("Notion")

    def applies_to(self, msg: RequestMessage):
        last_answer = get_last_answer(msg.user_id)
        if last_answer == "API_TOKEN_REQUEST" and get_token(msg.text) is not None:
            return True
        return save_requested(msg.text)

    def process(self, msg: RequestMessage) -> ResponseMessage:
        logger.info(f'Context saved for user {msg.user_id}')
        
        if not user_has_token(msg.user_id, self.app_id):
            token = get_token(msg.text)
            if token is None:
                return ResponseMessage(TOKEN_REQUEST_MESSAGE, "Notion", "API_TOKEN_REQUEST")
            else:
                save_secret(Secret(msg.user_id, self.app_id, TOKEN_SECRET_QUESTION, token))
                return ResponseMessage("I found a token in your message. I will use it to save messages in Notion for you.")
        
        try:
            url = add_entry_to_todays_page(msg.text)
            return ResponseMessage(f"I saved your message in Notion. You can find it here: {url}")
        except Exception as e:
            logger.error(f'Failed to save message to Notion: {e}')
            return ResponseMessage("I failed to save your message to Notion. Please try again later.")
        return ResponseMessage("I shall write this in runes Havi")