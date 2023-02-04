import os
import sys
sys.path.insert(1, os.getcwd())

import logging
import unittest

import notion_filter

class TestNotionFilter(unittest.TestCase):
    def test_get_token(self):
        actual = notion_filter.get_token("I got the secret secret_1234.")
        self.assertEqual(actual,"secret_1234")


    def test_save_requested(self):
        self.assertTrue(notion_filter.save_requested("Could you save this for me?"))
        self.assertTrue(notion_filter.save_requested("save"))
        self.assertTrue(notion_filter.save_requested("save that please"))


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    unittest.main()