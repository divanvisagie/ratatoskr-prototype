import logging
import os
import sys
sys.path.insert(1, os.getcwd())

import unittest

from clients.duckduck_client import DuckDuckGoClient

class DuckDuckClientTest(unittest.TestCase):

    def test_get_results(self):
        client = DuckDuckGoClient()
        results = client.get_duckduckgo_answer('Akka Documentation')
        print(results)


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    unittest.main()