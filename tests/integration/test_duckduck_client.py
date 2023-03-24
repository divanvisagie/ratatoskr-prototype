import logging
import os
import sys

from clients.duckduck_client import DuckDuckGoClient, result_to_markdown


logger = create_logger__name__)

def test_result_to_markdown():
    result = {
        'title': 'Akka Documentation',
        'body': 'Akka Documentation Website',
        'href': 'https://doc.akka.io/docs/akka/current/index.html'
    }
    actual = result_to_markdown(result)
    assert actual == '**[Akka Documentation](https://doc.akka.io/docs/akka/current/index.html)**\nAkka Documentation Website'

def test_duck_duck_go_client():
    client = DuckDuckGoClient()
    actual = client.search("Akka Documentation")
    logger.info(f"Got answer from DuckDuckGo: {actual}")
    assert len(actual) > 0