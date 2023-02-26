import logging
import os
import sys
sys.path.insert(1, os.getcwd())

import unittest

from clients.duckduck_client import DuckDuckGoClient, result_to_markdown


def test_result_to_markdown():
    result = {
        'title': 'Akka Documentation',
        'body': 'Akka Documentation Website',
        'href': 'https://doc.akka.io/docs/akka/current/index.html'
    }
    actual = result_to_markdown(result)
    assert actual == '**Akka Documentation**\n[Akka Documentation Website](https://doc.akka.io/docs/akka/current/index.html)'


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    unittest.main()