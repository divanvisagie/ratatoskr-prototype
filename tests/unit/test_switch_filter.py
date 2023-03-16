
import logging
from capability.duck_duck_go.filter import DuckDuckGoFilter

from capability.notion.capability import NotionFilter
from capability.chat_gpt.capability import ChatGptCapability
from capability.smart_switch.capability import get_target_filter


logger = logging.getLogger(__name__)

filters =  [ 
    NotionFilter(),
    DuckDuckGoFilter(),
    ChatGptCapability([]) 
]

def test_get_target_filter():
    actual = get_target_filter("save that please", filters)
    expected = "NotionFilter"
    assert actual == expected


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )