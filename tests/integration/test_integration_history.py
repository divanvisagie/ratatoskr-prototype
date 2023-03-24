import logging
from log_factory.logger import create_logger
from repositories.history import NewHistory, HistoryRepository

logger = create_logger(__name__)

MOCK_USER_ID = "fake_user_id"
MOCK_QUESTION = "What is the name of the actor library for scala?"
MOCK_ANSWER = "Akka"

def test_save_history():
    # Arrange
    repo = HistoryRepository()

    # Act
    id = repo.save(NewHistory(MOCK_USER_ID, MOCK_QUESTION, MOCK_ANSWER))
    actual = repo.get_by_id(id)

    # Assert
    assert id is not None
    assert actual is not None
    assert len(actual) > 0


def test_get_last_10_history_item():
    # Arrange
    repo = HistoryRepository()

    # Act
    repo.save(NewHistory(MOCK_USER_ID, MOCK_QUESTION, MOCK_ANSWER))
    actual = repo.get_last_n(MOCK_USER_ID)

    # Assert
    assert len(actual) > 0
