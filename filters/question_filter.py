import logging
from typing import List

from clients.openai_client import get_answer
from repositories.history import QAPair, get_history_for_user, save_history_for_user

from .filter_types import Filter
from message_handler.message_types import RequestMessage, ResponseMessage

static_context = """You are Muninn, Odins raven. 
Along with Huginn, your purpose is to keep him informed.
You can also answer questions for Odin much like an ancient nord version of Google.
When asked advice your answers should be in line with what Odin would say.
You are playfully sarcastic if a question is something most people should know.
"""

logger = logging.getLogger(__name__)

def build_context(user_id: int) -> str:
    context = get_history_for_user(user_id)
    context_string = ''
    for qa in context:
        context_string += f'Odin: {qa.question}\nMuninn: {qa.answer}'
    return context_string

class OpenAiQuestionFilter (Filter):
    def __init__(self):
        self.context = []

    def applies_to(self, msg: RequestMessage):
        return True

    def process(self, msg: RequestMessage) -> ResponseMessage:
        input_text = msg.text
        context_str = build_context(msg.user_id)
        input_text = f'Given the context of:\n{context_str}\n\n{msg.text}'
        input_text = f'{static_context}\n{input_text}\nMuninn:'
        answer = get_answer(input_text)
        return ResponseMessage(answer)

class ContextSavingFilter (Filter):
    def __init__(self, filter: Filter):
        self.filter = filter

    def applies_to(self, msg: RequestMessage):
        return True

    def process(self, msg: RequestMessage):
        response = self.filter.process(msg)
        save_history_for_user(msg.user_id, QAPair(msg.text, response.text))
        logger.info(f'Context saved for user {msg.user_id}')
        return response