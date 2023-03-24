import logging

import spacy
from capability.capability import Capability
from clients.duckduck_client import DuckDuckGoClient
from clients.openai_client import get_text_answer, AI_STOP_TOKEN, HUMAN_STOP_TOKEN
from clients.spacy_client import print_token_details
from log_factory.logger import create_logger
from message_handler.message_types import RequestMessage, ResponseMessage
from repositories.history import NewHistory, HistoryRepository


nlp = spacy.load("en_core_web_sm")

logger = create_logger(__name__)

def wrap_history(last_question: NewHistory, current_question: str):
    prompt = "Based on the following context, write a search engine query, output only the query itself:"
    middle = f"{HUMAN_STOP_TOKEN}:{last_question.question}\n{AI_STOP_TOKEN}:{last_question.answer}\n{HUMAN_STOP_TOKEN}:{current_question}"
    wrapped =  f"{prompt}\n\n{middle}"
    logger.info(f"Wrapped context: {wrapped}")
    return wrapped

def get_history(history_repository: HistoryRepository, user_id: str ) -> str:
    history = history_repository.get_by_id(user_id, 1)[0]
    return history

def asks_for_article_or_doc(message: str):
    doc = nlp(message)
    for token in doc:
        if token.text.lower() in {"documentation", "doc", "docs", "search", "find", "article"}:
            for child in token.children:
                print_token_details(child)
                if child.dep_ in {"prep", "det"}:
                    logger.info(f"Found relevant child: {child} for token {token}")
                    return True
    return False

class DuckDuckGoCapability(Capability):

    description = "Performs a search web on behalf of the user and returns the result, good for showing the user things, not good for summarising."

    def __init__(self):
        self.ddg_client = DuckDuckGoClient()
        self.history_repository = HistoryRepository()

    def relevance_to(self, msg: RequestMessage) -> float:
        if asks_for_article_or_doc(msg.text):
            return 1.0
        else:
            return 0.0

    def apply(self, msg: RequestMessage) -> ResponseMessage:
        try:
            history = get_history(self.history_repository, msg.user_id)
            wrapped = wrap_history(history, msg.text)
            logger.info(f"Asking OpenAI: {wrapped}")

            ddg_query_string = get_text_answer(wrapped)
            logger.info(f"Query: {ddg_query_string}")
            answer = self.ddg_client.search(ddg_query_string)

            # If answer is empty string
            if not answer:
                 # throw an exception
                answer = get_text_answer(f'The user has asked you to search for the term "{wrapped}" but nothing has been found on DuckDuckGo. Please provide a response.')
            
           
            return ResponseMessage(answer, "DuckDuckGo")
        except Exception as e:
            logger.error(f'Failed to search the web for that topic {e}')
            answer = "I don't know, I tried to search the web but I couldn't find anything"
            return ResponseMessage(answer, "DuckDuckGo")
