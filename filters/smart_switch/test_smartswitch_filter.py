
import logging
import os
from filters.duck_duck_go.ddg_filter import DuckDuckFilter

from message_handler.message_types import RequestMessage
from filters.notion.notion_filter import NotionFilter
from filters.question_filter import OpenAiQuestionFilter

from smartswitch_filter import SmartSwitchFilter, build_filter_list, filter_to_description, get_target_filter

logger = logging.getLogger(__name__)

filters =  [ 
    NotionFilter(),
    DuckDuckFilter(),
    OpenAiQuestionFilter([]) 
]

def assertLineByLine(actual: str, expected: str):
    actual_lines = actual.split(os.linesep)
    expected_lines = expected.split(os.linesep)
    for actual_line, expected_line in zip(actual_lines, expected_lines):
        logger.info(f"\nActual: {actual_line}\nExpected: {expected_line}\n")
        assert actual_line == expected_line

def test_get_target():
    filter = SmartSwitchFilter()
    req = RequestMessage("save that please", 1)
    res = filter.process(req)
    logger.info(f"Response: {res}")
    assert res.text == "NotionFilter"

def test_filter_to_description():
    filter = NotionFilter()
    actual = filter_to_description(filter)
    assert actual == "NotionFilter: Will save the last message the bot returned to notion for the user"

def test_get_target_filter():
    actual = get_target_filter("save that please", filters)
    expected = "NotionFilter"
    assert actual == expected


def test_build_filter_list():
    actual = build_filter_list(filters)
    expected = [
        "NotionFilter: Will save the last message the bot returned to notion for the user",
        "DuckDuckFilter: Performs a search on behalf of the user",
        "OpenAiQuestionFilter: Will respond naturally to a users prompt but cannot search the web for links",
    ]
    assertLineByLine(actual, os.linesep.join(expected))

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )