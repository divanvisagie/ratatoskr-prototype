import logging
import os
import sys
sys.path.insert(1, os.getcwd())

import unittest

from clients.duckduck_client import DuckDuckGoClient, result_to_markdown

class DuckDuckClientTest(unittest.TestCase):

    # def test_get_results(self):
    #     client = DuckDuckGoClient()
    #     results = client.get_duckduckgo_answer('Akka Documentation')
    #     print(results)

    def test_result_to_markdown(self):
        result = {
            'title': 'Akka Documentation',
            'body': 'Akka Documentation Website',
            'href': 'https://doc.akka.io/docs/akka/current/index.html'
        }
        actual = result_to_markdown(result)
        self.assertEquals(actual, '**Akka Documentation**\n[Akka Documentation Website](https://doc.akka.io/docs/akka/current/index.html)')


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    unittest.main()