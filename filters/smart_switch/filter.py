import os
from typing import List
from clients.openai_client import get_text_answer
from filters.duck_duck_go.filter import DuckDuckFilter
from filters.filter_types import Filter
from filters.notion.notion_filter import NotionFilter
from filters.question_filter import OpenAiQuestionFilter
from message_handler.message_types import RequestMessage, ResponseMessage

def get_prompt(question, filters: str):
    prompt = f"""I have a list of classes that perform different tasks for a user

    {filters}

    Given the following conversation:

    User: {question}

    In one word with no punctuation, which filter should be used?"""

    return prompt

def get_target_filter(text: str, filters: List[Filter]):
    filter_str = build_filter_list(filters)
    prompt = get_prompt(text, filter_str)
    answer = get_text_answer(prompt).strip()
    return answer

def filter_to_description(filter: Filter):
    return f'{filter.__class__.__name__}: {filter.description}'

def build_filter_list(filters: List[Filter]):
    descriptions =  [filter_to_description(filter) for filter in filters]
    return os.linesep.join(descriptions)

class SmartSwitchFilter(Filter):
    """Uses response from openai to determine which filter to use"""
    def __init__(self):
        self.filters: List[Filter] = [
            # NotionFilter(),
            DuckDuckFilter(),
            OpenAiQuestionFilter([])
        ]
    
    def applies_to(self, msg: RequestMessage):
        return True
    
    def process(self, msg: RequestMessage) -> ResponseMessage:
        filter = get_target_filter(msg.text, self.filters)
        for f in self.filters:
            if f.__class__.__name__ == filter:
                return f.process(msg)

        return  ResponseMessage("Unfortunately I cant find anything to do", self.__class__.__name__)