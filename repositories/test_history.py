import logging
from repositories.history import NewHistory, HistoryRepository

logger = logging.getLogger(__name__)

def test_save_history():
    repo = HistoryRepository()
    repo.save(1, NewHistory("What is the name of the actor library for scala?", "Akka"))
    pass


def test_recall_order():
    """Given multiple history items, the most recent should be returned last"""
    # Arrange
    repo = HistoryRepository()
    repo.delete_all(1)
    repo.save(1, NewHistory("This is the first question", "This is the first answer", responder="unit_test"))
    repo.save(1, NewHistory("This is the second question", "This is the second answer", responder="unit_test"))
    repo.save(1, NewHistory("This is the third question", "This is the third answer", responder="unit_test"))
    repo.save(1, NewHistory("This is the fourth question", "This is the fourth answer", responder="unit_test"))

    # Act
    history = repo.get_by_id(1, 10)


    # Assert
    for item in history:
        logger.info(f"History: {item}")
    
    assert len(history) == 4
    assert history[0].question == "This is the first question"
    assert history[1].question == "This is the second question"
    assert history[2].question == "This is the third question"
    assert history[3].question == "This is the fourth question"


if __name__ == '__main__':
    print(f"Running as main: {__name__}")
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )