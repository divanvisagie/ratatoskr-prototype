import logging
import os
import sys
sys.path.insert(1, os.getcwd())
from repositories.user import UserRepository

logger = logging.getLogger(__name__)

def test_get_by_id():
    """Given a user id, return the user"""
    # Arrange
    repo = UserRepository()

    # Act
    user = repo.get_by_telegram_username("UNIT_TEST")
    logger.info(f"User: {user}")

    # Assert
    assert user is not None
    assert user.id == 1
    assert user.telegram_username == "UNIT_TEST"
    assert user.access_level == 0


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    test_get_by_id()