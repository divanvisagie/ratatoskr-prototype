from typing import List

from clients.openai_client import get_answer
from repositories.history import QAPair, get_history_for_user, save_history_for_user

from .filter_types import Filter
from message_handler.message_types import RequestMessage

static_context = """You are Muninn, Odins raven. 
Along with Huginn, your purpose is to keep him informed.
You eat the corpses of the dead and bring back their memories to Odin.
"""
BUFFER_SIZE = 100




def build_context(user_id: int) -> str:
    context = get_history_for_user(user_id)
    context_string = ''
    for qa in context:
        context_string += f'Odin: {qa.question}\nMuninn: {qa.answer}'
    return context_string

class QuestionFilter (Filter):
    def __init__(self):
        self.context = []

    def applies_to(self, msg: RequestMessage):
        return True

    def process(self, msg: RequestMessage):
        input_text = msg.text
        context_str = build_context(msg.user_id)
        input_text = f'Given the context of:\n{context_str}\n\n{msg.text}'
        input_text = f'{static_context}\n{input_text}\nMuninn:'

        answer = get_answer(input_text)

        if len(self.context) > BUFFER_SIZE:
            self.context.pop(0)
        save_history_for_user(msg.user_id, QAPair(msg.text, answer))

        return answer
