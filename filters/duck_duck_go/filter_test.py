import os
import sys
sys.path.insert(1, os.getcwd())

import logging
import unittest
from filters.duck_duck_go.filter import DuckDuckFilter
from message_handler.message_types import RequestMessage

positive_sentences = [
    "Do you have documentation for this?",
    "Can you find the documentation?",
]


class TestNotionFilter(unittest.TestCase):

    def test_applies_to(self):
        filter = DuckDuckFilter()
        for sentence in positive_sentences:
            msg = RequestMessage(
                sentence, 
                1
            )
            actual = filter.applies_to(msg)
            self.assertTrue(actual)

    def test_applies_to_negative(self):
        filter = DuckDuckFilter()
        msg = RequestMessage(
            "Save that", 
            1
        )
        actual = filter.applies_to(msg)
        self.assertFalse(actual)

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    unittest.main()


