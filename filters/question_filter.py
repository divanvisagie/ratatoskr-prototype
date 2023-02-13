import logging
from typing import List

from clients.openai_client import AI_STOP_TOKEN, HUMAN_STOP_TOKEN, get_code_answer, get_text_answer
from clients.spacy_client import question_is_about_code
from repositories.history import History, HistoryRepository

from .filter_types import Filter
from message_handler.message_types import RequestMessage, ResponseMessage

static_context = """You are Muninn, Odin's raven. You know him as Hávi
Along with Huginn, your purpose is to keep him informed.
You can also answer questions for Hávi much like an ancient nord version of Google.
When asked advice your answers should be in line with what Hávi would say.
You are playfully sarcastic if a question is something most people should know.
"""

logger = logging.getLogger(__name__)

def build_context_from_history(user_id: int) -> str:
    history_repository = HistoryRepository()
    context = history_repository.get_by_id(user_id)
    context_string = ''
    for qa in context:
        context_string += f'{HUMAN_STOP_TOKEN}: {qa.question}\n{AI_STOP_TOKEN}: {qa.answer}'
    return context_string

class OpenAiQuestionFilter (Filter):
    def __init__(self, filters: List[Filter]):
        self.filters = filters

    def applies_to(self, msg: RequestMessage):
        """ We want to apply this filter right at the end so its always true"""
        return True

    def process(self, msg: RequestMessage) -> ResponseMessage:
        for filter in self.filters:
            if filter.applies_to(msg):
                return filter.process(msg)
        
        input_text = msg.text
        context_str = build_context_from_history(msg.user_id)
        input_text = f'Given the context of:\n{context_str}\n\n{msg.text}'
        input_text = f'{static_context}\n{input_text}\nMuninn:'
        answer = get_text_answer(input_text)
        return ResponseMessage(answer)
