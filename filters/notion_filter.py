import logging
import spacy
import re

from clients.notion_service_client import add_entry_to_todays_page
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
JOURNAL_DATABASE_REQUEST_MESSAGE = """
I don't know which database to save your messages in. 
Please send me the URL of the database you want to save your messages in.
"""
TOKEN_SECRET_QUESTION = "Notion API Token"
JOURNAL_DATABASE_QUESTION = "Notion Journal Database"

API_TOKEN_REQUEST = "API_TOKEN_REQUEST"
JOURNAL_DATABASE_REQUEST = "JOURNAL_DATABASE_REQUEST"

logger = logging.getLogger(__name__)
nlp = spacy.load("en_core_web_sm")

def user_has_token(user_id: int, app_id: int, token: str) -> bool:
    secret = get_app_secret_for_user(user_id, app_id, token)
    if secret is not None:
        return True
    return False

def extract_token_from_message(msg: str) -> str:
    doc = nlp(msg)
    for token in doc:
        if token.text.startswith('secret_'):
            return token.text
    return None

def extract_database_from_message(msg: str) -> str:
    try:
        match = re.search("/([a-zA-Z0-9]+?)\?", msg)
        return match.group(1)
    except:
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
        if last_answer == API_TOKEN_REQUEST and extract_token_from_message(msg.text) is not None:
            return True
        if last_answer == JOURNAL_DATABASE_REQUEST and extract_database_from_message(msg.text) is not None:
            return True
        return save_requested(msg.text)

    def process(self, msg: RequestMessage) -> ResponseMessage:
        logger.info(f'Context saved for user {msg.user_id}')
        
        if get_app_secret_for_user(msg.user_id, self.app_id, TOKEN_SECRET_QUESTION) is None:
            token = extract_token_from_message(msg.text)
            if token is None:
                return ResponseMessage(
                    TOKEN_REQUEST_MESSAGE, 
                    "Notion", 
                    API_TOKEN_REQUEST
                )
            else:
                save_secret(Secret(msg.user_id, self.app_id, TOKEN_SECRET_QUESTION, token))
                return ResponseMessage("I found a token in your message. I will use it to save messages in Notion for you.")
        
        if get_app_secret_for_user(msg.user_id, self.app_id, JOURNAL_DATABASE_QUESTION) is None:
            database_id = extract_database_from_message(msg.text)
            if database_id is None:
                return ResponseMessage(
                    JOURNAL_DATABASE_REQUEST_MESSAGE, 
                    "Notion", 
                    JOURNAL_DATABASE_REQUEST
                )
            else:
                save_secret(Secret(msg.user_id, self.app_id, JOURNAL_DATABASE_QUESTION, database_id))
                return ResponseMessage("I found a database in your message. I will use it to save messages in Notion for you.")

        try:
            url = add_entry_to_todays_page(msg.text)
            return ResponseMessage(f"I saved your message in Notion. You can find it here: {url}")
        except Exception as e:
            logger.error(f'Failed to save message to Notion: {e}')
            return ResponseMessage("I failed to save your message to Notion. Please try again later.")
