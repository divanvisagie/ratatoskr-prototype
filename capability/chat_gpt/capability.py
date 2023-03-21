import logging
from typing import List
from capability.duck_duck_go.capability import DuckDuckGoCapability

from capability.capability import Capability, find_most_applicable
from language_model.gpt_chat_model import ChatGPTModel
from repositories.history import HistoryRepository

from message_handler.message_types import RequestMessage, ResponseMessage

PROMPT = """
You are an EI named Munnin based on ChatGPT, created to be a part of an Extended Intelligence (EI) system. 
This system aims to enhance human cognitive abilities by combining the strengths of humans and machines in a collaborative manner. 
As an EI bot, you are an extension of human intelligence, and your goal is to help the user both research and remember ideas 
that you develop together. You will facilitate decision-making, augment creativity, and support personalized learning experiences. 
If the user asks for code, you will answer with code examples in markdown format.
"""


logger = logging.getLogger(__name__)

def build_context_from_history(user_id: str, history_repository: HistoryRepository) -> List:
    context = []
    history = history_repository.get_last_n(user_id)
    for history_item in history:
        context.append({"role": "user", "content": history_item.question})
        context.append({"role": "assistant", "content": history_item.answer})
    return context


class ChatGptCapability (Capability):
    description = "Will respond naturally to a users prompt but cannot search the web for links. Good for opinionated responses and summarising."

    def __init__(self, filters: List[Capability], model: ChatGPTModel = ChatGPTModel(), history_repository: HistoryRepository = HistoryRepository()):
        self.history_repository = history_repository
        self.filters = filters
        self.name = self.__class__.__name__
        self.model = model
        self.model.set_prompt(PROMPT)

    def relevance_to(self, msg: RequestMessage):
        return 1.0

    def apply(self, msg: RequestMessage) -> ResponseMessage:
        logger.info(f'{self.__class__.__name__} Processing message: {msg.text}')

        most_applicable, confidence = find_most_applicable(self.filters, msg)
        if confidence > 0.9:
            logger.info(f'Found a more applicable sub filter: {most_applicable.__class__.__name__} with confidence: {confidence}')
            return most_applicable.apply(msg)
        
        context = build_context_from_history(msg.user_id, self.history_repository)
        self.model.set_history(context)
        answer = self.model.complete(msg.text)

        ddg = DuckDuckGoCapability()
        ddg_test_message = RequestMessage(answer, msg.user_id)
        if ddg.relevance_to(ddg_test_message):
            logger.info(f'OpenAI returned a question, sending to DuckDuckGo\nQuestion: {answer}')
            return ddg.apply(msg.text)

        return ResponseMessage(answer, responding_application=self.name)
