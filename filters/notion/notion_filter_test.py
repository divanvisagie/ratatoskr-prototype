import os
import sys
sys.path.insert(1, os.getcwd())

import logging
import unittest

import notion_filter

class TestNotionFilter(unittest.TestCase):
    def test_get_token(self):
        actual = notion_filter.extract_token_from_message("I got the secret secret_1234.")
        self.assertEqual(actual,"secret_1234")

    def test_save_requested(self):
        self.assertTrue(notion_filter.save_requested("Could you save this for me?"))
        self.assertTrue(notion_filter.save_requested("save"))
        self.assertTrue(notion_filter.save_requested("save that please"))

    def test_extract_database_from_message(self):
        actual = notion_filter.extract_database_from_message("i got this https://www.notion.so/d2b36ebe405740ecab150b9e8b1ed50a?v=58d3b2314c0e493b80219c2250304e04")
        self.assertEqual(actual,"d2b36ebe405740ecab150b9e8b1ed50a")
        actual = notion_filter.extract_database_from_message("cheese")
        self.assertIsNone(actual)

    def test_should_save_previous_message(self):
        actual = notion_filter.should_save_previous_message("save that please")
        self.assertTrue(actual)
        actual = notion_filter.should_save_previous_message("save this: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        self.assertFalse(actual)

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    unittest.main()