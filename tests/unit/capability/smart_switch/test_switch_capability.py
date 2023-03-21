
import logging
from capability.duck_duck_go.capability import DuckDuckGoCapability

from capability.notion.capability import NotionCapability
from capability.chat_gpt.capability import ChatGptCapability
from capability.smart_switch.capability import get_target_filter


logger = logging.getLogger(__name__)

filters =  [ 
    NotionCapability(),
    DuckDuckGoCapability(),
    ChatGptCapability([]) 
]

def test_given_save_question_get_target_filter_returns_NotionCapability():
    actual = get_target_filter("save that please", filters)
    expected = "NotionCapability"
    assert actual == expected


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )