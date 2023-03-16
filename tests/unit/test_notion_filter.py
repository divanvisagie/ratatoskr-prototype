

from capability.notion.capability import NotionFilter, extract_database_from_message, extract_token_from_message, should_save_previous_message
from capability.notion.model import save_requested
from message_handler.message_types import RequestMessage

import logging


def test_get_token():
    actual = extract_token_from_message("I got the secret secret_1234.")
    assert actual == "secret_1234"

def test_save_requested():
    assert save_requested("Could you save this for me?") == True
    assert save_requested("save") == True
    assert save_requested("save that please") == True

def test_extract_database_from_message():
    actual = extract_database_from_message("i got this https://www.notion.so/d2b36ebe405740ecab150b9e8b1ed50a?v=58d3b2314c0e493b80219c2250304e04")
    assert actual == "d2b36ebe405740ecab150b9e8b1ed50a"
    actual = extract_database_from_message("cheese")
    assert actual is None

def test_should_save_previous_message():
    actual = should_save_previous_message("save that please")
    assert actual == True
    actual = should_save_previous_message("save this: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert actual == False
    
def test_applies_to():
    # Arrange
    rm = RequestMessage("save that please", 1)
    nf = NotionFilter()
    assert nf.relevance_to(rm) == True
if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )