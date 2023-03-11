import logging
from repositories.history import NewHistory, HistoryRepository

logger = logging.getLogger(__name__)

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


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )