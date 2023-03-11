
import logging
from filters.duck_duck_go.filter import DuckDuckFilter

from filters.notion.filter import NotionFilter
from filters.chat_gpt.filter import OpenAiQuestionFilter
from filters.smart_switch.filter import get_target_filter


logger = logging.getLogger(__name__)

filters =  [ 
    NotionFilter(),
    DuckDuckFilter(),
    OpenAiQuestionFilter([]) 
]

def test_get_target_filter():
    actual = get_target_filter("save that please", filters)
    expected = "NotionFilter"
    assert actual == expected


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )