import logging
import spacy
import re

from clients.notion_service_client import add_entry_to_todays_page
from filters.filter_types import Filter
from filters.notion.api_token_filter import MissingTokenFilter
from filters.notion.model import save_requested
from message_handler.message_types import RequestMessage, ResponseMessage
from repositories.app import AppRepository
from repositories.history import HistoryRepository
from repositories.secret import Secret, SecretRepository
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

JOURNAL_DATABASE_REQUEST = "JOURNAL_DATABASE_REQUEST"

API_TOKEN_REQUEST = "API_TOKEN_REQUEST"

logger = logging.getLogger(__name__)
nlp = spacy.load("en_core_web_sm")

def user_has_token(user_id: int, app_id: int, token: str) -> bool:
    secret_repository = SecretRepository()
    secret = secret_repository.get_app_secret_for_user(user_id, app_id, token)
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

def should_save_previous_message(question: str) -> bool:
    doc = nlp(question)
    for token in doc:
      if token.pos_ == "PROPN":
        return False
    return True

class NotionFilter (Filter):
    description = "Will save the last message the bot returned to notion for the user"

    def __init__(self):
        self.app_repository = AppRepository()
        app_id = self.app_repository.get_id_by_name("Notion")
        self.app_id = app_id
        self.history_repository = HistoryRepository()
        self.filters = [
            MissingTokenFilter(app_id, API_TOKEN_REQUEST, TOKEN_REQUEST_MESSAGE, extract_token_from_message),
            MissingTokenFilter(app_id, JOURNAL_DATABASE_REQUEST, JOURNAL_DATABASE_REQUEST_MESSAGE, extract_database_from_message)
        ]

    def applies_to(self, msg: RequestMessage):
        try:
            applies_to_subfilter = False
            for filter in self.filters:
                if filter.applies_to(msg):
                    logger.info(f'Applies to subfilter {filter}')
                    applies_to_subfilter = True
        
            return applies_to_subfilter | save_requested(msg.text)
        except Exception as e:
            logger.error(f'Failed to determine if filter applies: {e}')
            return False

    def process(self, msg: RequestMessage) -> ResponseMessage:
        logger.info(f'Context saved for user {msg.user_id}')
        
        for filter in self.filters:
            if filter.applies_to(msg):
                logger.info(f'Applying subfilter {filter}')
                return filter.process(msg)

        message_to_save = msg.text
        if should_save_previous_message(msg.text):
            message_to_save = self.history_repository.get_by_id(msg.user_id, 1)[0].answer

        try:
            url = add_entry_to_todays_page(message_to_save)
            return ResponseMessage(f"I saved your message in Notion. You can find it here: {url}", responding_application="Notion")
        except Exception as e:
            logger.error(f'Failed to save message to Notion: {e}')
            return ResponseMessage("I failed to save your message to Notion. Please try again later.")
