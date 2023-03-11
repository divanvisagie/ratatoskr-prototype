import logging
from repositories.user import NewUser, UserRepository

logger = logging.getLogger(__name__)

def test_get_by_id():
    """Given a user id, return the user"""
    # Arrange
    repo = UserRepository()
    user = NewUser("UNIT_TEST", 1)

    # Act
    user_id = repo.save(user)
    user = repo.get_by_id(user_id)

    # Assert
    assert user is not None
    assert user.telegram_username == "UNIT_TEST"
    assert user.access_level == 1

    repo.deleteByTelegramUsername("UNIT_TEST")


def test_get_by_telegram_username():
    """Given a user, save the user"""
    # Arrange
    repo = UserRepository()
    user = NewUser("UNIT_TEST", 1)

    # Act
    repo.save(user)
    user = repo.get_by_telegram_username("UNIT_TEST")

    # Assert
    assert user is not None
    assert user.telegram_username == "UNIT_TEST"
    assert user.access_level == 1

    repo.deleteByTelegramUsername("UNIT_TEST")

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )