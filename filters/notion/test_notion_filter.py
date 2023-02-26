import os
import sys
from filters.notion.notion_filter import NotionFilter

from message_handler.message_types import RequestMessage
sys.path.insert(1, os.getcwd())

import logging
import unittest

import notion_filter


def test_get_token():
    actual = notion_filter.extract_token_from_message("I got the secret secret_1234.")
    assert actual == "secret_1234"

def test_save_requested():
    assert notion_filter.save_requested("Could you save this for me?") == True
    assert notion_filter.save_requested("save") == True
    assert notion_filter.save_requested("save that please") == True

def test_extract_database_from_message():
    actual = notion_filter.extract_database_from_message("i got this https://www.notion.so/d2b36ebe405740ecab150b9e8b1ed50a?v=58d3b2314c0e493b80219c2250304e04")
    assert actual == "d2b36ebe405740ecab150b9e8b1ed50a"
    actual = notion_filter.extract_database_from_message("cheese")
    assert actual is None

def test_should_save_previous_message():
    actual = notion_filter.should_save_previous_message("save that please")
    assert actual == True
    actual = notion_filter.should_save_previous_message("save this: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert actual == False
    
def test_applies_to():
    # Arrange
    rm = RequestMessage("save that please", 1)
    nf = NotionFilter()
    assert nf.applies_to(rm) == True
if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    unittest.main()