import os
import sys
sys.path.insert(1, os.getcwd())

import logging
import unittest
import notion_service_client



def test_create_database():
    assert (notion_service_client.create_database()) == True

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    unittest.main()