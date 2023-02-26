import logging

import spacy
from clients.duckduck_client import DuckDuckGoClient
from clients.openai_client import get_text_answer
from clients.spacy_client import print_token_details
from filters.filter_types import Filter
from message_handler.message_types import RequestMessage, ResponseMessage
from repositories.history import History, HistoryRepository


nlp = spacy.load("en_core_web_sm")

logger = logging.getLogger(__name__)

def wrap_history(last_question: History, current_question: str):
    prompt = "Based on the following context, write a search engine query, output only the query itself:"
    middle = f"User:{last_question.question}\nBot:{last_question.answer}\nUser:{current_question}"
    wrapped =  f"{prompt}\n\n{middle}"
    logger.info(f"Wrapped context: {wrapped}")
    return wrapped


class DuckDuckFilter(Filter):
    def __init__(self):
        self.ddg_client = DuckDuckGoClient()
        self.history_repository = HistoryRepository()

    def applies_to(self, msg: RequestMessage):
        doc = nlp(msg.text)
     
        for token in doc:
            if token.text.lower() in {"documentation", "doc", "docs", "search", "find", "article"}:
                for child in token.children:
                    print_token_details(child)
                    if child.dep_ in {"prep", "det"}:
                        logger.info(f"Found relevant child: {child} for token {token}")
                        return True
        
        return False

    def process(self, msg: RequestMessage) -> ResponseMessage:
        try:
            logger.info(f'Context saved for user {msg.user_id}')
            
            last_qa_pair = self.history_repository.get_by_id(msg.user_id,1)[0]
            wrapped = wrap_history(last_qa_pair, msg.text)
            logger.info(f"Wrapped context: {wrapped}")

            ddg_query = get_text_answer(wrapped)
            logger.info(f"Query: {ddg_query}")
            answer = self.ddg_client.get_duckduckgo_answer(ddg_query)

            # If answer is empty string
            if not answer:
                 # throw an exception
                raise Exception("No answer found")

            return ResponseMessage(answer, "DuckDuckGo")
        except Exception as e:
            logger.error(f'Failed to searcht the web for that topic')
            answer = "I don't know, I tried to search the web but I couldn't find anything"
            return ResponseMessage(answer, "DuckDuckGo")
