import logging
import unittest

from repositories.history import History, HistoryRepository


logger = logging.getLogger(__name__)

def test_save_history():
    repo = HistoryRepository()
    repo.save(1, History("What is the name of the actor library for scala?", "Akka"))
    pass


if __name__ == '__main__':
    print(f"Running as main: {__name__}")
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
