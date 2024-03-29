import spacy
import re

from capability.capability import Capability, find_most_applicable
from clients.notion_service_client import add_entry_to_todays_page
from capability.notion.api_token_filter import MissingTokenFilter
from capability.notion.model import save_requested
from log_factory.logger import create_logger
from message_handler.message_types import RequestMessage, ResponseMessage
from repositories.history import HistoryRepository
from repositories.secret import SecretRepository

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

logger = create_logger(__name__)
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

class NotionCapability (Capability):
    description = "Will save the last message the bot returned to notion for the user, should only be used if the user explicitly asks to save"

    def __init__(self):
        super().__init__()
        self.history_repository = HistoryRepository()
        self.filters = [
            MissingTokenFilter(API_TOKEN_REQUEST, TOKEN_REQUEST_MESSAGE, extract_token_from_message),
            MissingTokenFilter(JOURNAL_DATABASE_REQUEST, JOURNAL_DATABASE_REQUEST_MESSAGE, extract_database_from_message)
        ]

    def relevance_to(self, msg: RequestMessage) -> float:
        try:
            filter, subfilter_relevance = find_most_applicable(self.filters, msg)
            filter_relevance = save_requested(msg.text)
            if filter_relevance > subfilter_relevance:
                return filter_relevance
            else:
                return subfilter_relevance
            
        except Exception as e:
            logger.error(f'Failed to determine if filter applies: {e}')
            return 0.0

    def apply(self, msg: RequestMessage) -> ResponseMessage:
        logger.info(f'Context saved for user {msg.user_id}')
        
        filter, subfilter_relevance = find_most_applicable(self.filters, msg)
        if subfilter_relevance > 0.9:
            logger.info(f'Applying subfilter {filter}')
            return filter.apply(msg)
        
        message_to_save = msg.text
        if should_save_previous_message(msg.text):
            message_to_save = self.history_repository.get_by_id(msg.user_id)[0].answer

        try:
            url = add_entry_to_todays_page(message_to_save)
            return ResponseMessage(f"I saved your message in Notion. You can find it here: {url}", responding_application="Notion")
        except Exception as e:
            logger.error(f'Failed to save message to Notion: {e}')
            return ResponseMessage("I failed to save your message to Notion. Please try again later.")
