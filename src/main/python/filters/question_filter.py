import logging
from typing import List

from clients.openai_client import AI_STOP_TOKEN, HUMAN_STOP_TOKEN, get_code_answer, get_text_answer
from clients.spacy_client import question_is_about_code
from filters.duck_duck_go.filter import DuckDuckFilter
from language_model.gpt2_model import GPT2Model
from language_model.gpt3_model import GPT3CompletionModel
from language_model.base_model import BaseModel
from language_model.gpt_chat_model import GPTChatModel
from language_model.named_transformers_model import NamedModel
from repositories.history import NewHistory, HistoryRepository

from .filter_types import Filter
from message_handler.message_types import RequestMessage, ResponseMessage

static_context = """You are a bot who is created to helpfully answer a user's questions
You have the personality of Muninn, Odin's raven. You know Odin as Hávi and address the user as if they are Hávi.
You can have an opinion but are open to being corrected.
You are playfully sarcastic if a question is something most people should know.
You make jokes about the game Portal and pretend to be GLaDOS if the user keeps referring to "testing".
"""

logger = logging.getLogger(__name__)

def build_context_from_history(user_id: int) -> str:
    history_repository = HistoryRepository()
    context = history_repository.get_by_id(user_id)
    context_string = ''
    for qa in context:
        context_string += f'{HUMAN_STOP_TOKEN}: {qa.question}\n\n{AI_STOP_TOKEN}: {qa.answer}'
    return context_string

class OpenAiQuestionFilter (Filter):
    description = "Will respond naturally to a users prompt but cannot search the web for links. Good for opinionated responses and summarising."

    def __init__(self, filters: List[Filter]):
        self.filters = filters
        self.name = self.__class__.__name__
        self.model: BaseModel = GPTChatModel("You are ChatGPT, a large language model trained by OpenAI. You answer questions and when the user asks code questions, you will answer with code examples in markdown format.")
    def applies_to(self, msg: RequestMessage):
        """ We want to apply this filter right at the end so its always true"""
        return True

    def process(self, msg: RequestMessage) -> ResponseMessage:
        user_query = msg.text
        logger.info(f'{self.__class__.__name__} Processing message: {user_query}')
        for filter in self.filters:
            if filter.applies_to(msg):
                return filter.process(msg)
        
        historical_context = build_context_from_history(msg.user_id)
        chat_context = f'Given the context of:\n{historical_context}\n'
        input_text = f'{static_context}\n{chat_context}\n{HUMAN_STOP_TOKEN}: {msg.text}\n{AI_STOP_TOKEN}:'

        logger.info(f'Sending the following text to OpenAI:\n{input_text}')
        answer = self.model.complete(msg.text)

        ddg = DuckDuckFilter()
        ddg_test_message = RequestMessage(answer, msg.user_id)
        if ddg.applies_to(ddg_test_message):
            logger.info(f'OpenAI returned a question, sending to DuckDuckGo\nQuestion: {answer}')
            return ddg.process(msg.text)

        return ResponseMessage(answer, responding_application=self.name)
