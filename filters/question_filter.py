from typing import List

from clients.openai_client import get_answer

from .filter_types import Filter
from message_handler.message_types import RequestMessage

static_context = 'You are Muninn, Odins raven. Your purpose is to keep him informed.'
BUFFER_SIZE = 100


class QAPair ():
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

def build_context(context: List[QAPair]) -> str:
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
        if len(self.context) > 0:
            context_str = build_context(self.context)
            input_text = f'Given the context of:\n{context_str}\n\n{msg.text}'
        input_text = f'{static_context}\n{input_text}'

        answer = get_answer(input_text)

        if len(self.context) > BUFFER_SIZE:
            self.context.pop(0)
        self.context.append(QAPair(msg.text, answer))

        return answer
