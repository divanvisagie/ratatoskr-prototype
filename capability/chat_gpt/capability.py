import logging
from typing import List

from capability.duck_duck_go.capability import DuckDuckGoCapability

from capability.capability import Capability, find_most_applicable
from language_model.gpt_chat_model import ChatGPTModel
from log_factory.logger import create_logger
from repositories.history import HistoryRepository

from message_handler.message_types import RequestMessage, ResponseMessage

logger = create_logger(__name__)

def build_context_from_history(user_id: str, history_repository: HistoryRepository) -> List:
    context = []
    history = history_repository.get_last_n(user_id,20)
    for history_item in history:
        context.append({"role": "user", "content": history_item.question})
        context.append({"role": "assistant", "content": history_item.answer})
    return context


def get_prompt_from_file(prompt_file: str) -> str:
    with open(prompt_file, 'r') as f:
        prompt = f.read()
    return prompt


class ChatGptCapability (Capability):
    description = "Will respond naturally to a users prompt but cannot search the web for links. Good for opinionated responses and summarising."

    def __init__(self, filters: List[Capability], history_repository: HistoryRepository = HistoryRepository()):
        super().__init__()
        self.history_repository = history_repository
        self.filters = filters
        self.name = self.__class__.__name__
        self.model = ChatGPTModel(
            get_prompt_from_file('capability/chat_gpt/prompt.txt')
        )

    def relevance_to(self, msg: RequestMessage):
        return 1.0

    def apply(self, msg: RequestMessage) -> ResponseMessage:
        with msg.tracer.start_as_current_span(f'{self.__class__.__name__}.apply'):
            logger.info(f'{self.__class__.__name__} Processing message: {msg.text}')

            most_applicable, confidence = find_most_applicable(self.filters, msg)
            if confidence > 0.9:
                logger.info(f'Found a more applicable sub filter: {most_applicable.__class__.__name__} with confidence: {confidence}')
                return most_applicable.apply(msg)
            
            context = build_context_from_history(msg.user_id, self.history_repository)
            self.model.set_history(context)
            answer = self.model.complete(msg.text, msg.tracer)

            ddg = DuckDuckGoCapability()
            ddg_test_message = RequestMessage(answer, msg.user_id)
            if ddg.relevance_to(ddg_test_message):
                logger.info(f'OpenAI returned a question, sending to DuckDuckGo\nQuestion: {answer}')
                return ddg.apply(msg.text)

            return ResponseMessage(answer, responding_application=self.name)
