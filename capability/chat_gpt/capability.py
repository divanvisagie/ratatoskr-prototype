import logging
from typing import List
from capability.duck_duck_go.capability import DuckDuckGoCapability

from capability.capability import Capability, find_most_applicable
from language_model.gpt_chat_model import ChatGPTModel
from repositories.history import HistoryRepository

from message_handler.message_types import RequestMessage, ResponseMessage

static_context = """You are a bot who is created to helpfully answer a user's questions
You have the personality of Muninn, Odin's raven. You know Odin as Hávi and address the user as if they are Hávi.
You can have an opinion but are open to being corrected.
You are playfully sarcastic if a question is something most people should know.
You make jokes about the game Portal and pretend to be GLaDOS if the user keeps referring to "testing".
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
        self.model.set_prompt("You are ChatGPT, a large language model trained by OpenAI. You answer questions and when the user asks code questions, you will answer with code examples in markdown format.")

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
