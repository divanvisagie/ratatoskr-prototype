from clients.openai_client import get_code_answer
from clients.spacy_client import question_is_about_code
from filters.filter_types import Filter
from message_handler.message_types import RequestMessage, ResponseMessage


class OpenAiCodeGenFilter(Filter):
    def __init__(self):
        pass

    def applies_to(self, msg: RequestMessage):
        answer = question_is_about_code(msg.text)
        print(f'Question is about code: {answer}')
        return answer

    def process(self, msg: RequestMessage) -> ResponseMessage:
        answer = get_code_answer(msg.text)
        return ResponseMessage(answer)