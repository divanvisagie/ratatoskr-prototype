from repositories.user import UserRepository, NewUser

TEST_TELEGRAM_USERNAME="test_user"

def test_UserRepository_save_given_user_saves_user_to_database():
    # Arrange
    user = NewUser(
        telegram_username=TEST_TELEGRAM_USERNAME,
        access_level=1
    )
    repository = UserRepository()

    # Act
    id = repository.save(user)

    # Assert
    assert id is not None
    actual = repository.get_by_id(id)
    assert actual is not None
    assert actual.telegram_username == TEST_TELEGRAM_USERNAME

def test_UserRepository_get_user_by_telegram_name():
    # Arrange
    user = NewUser(
        telegram_username=TEST_TELEGRAM_USERNAME,
        access_level=1
    )
    repository = UserRepository()
    id = repository.save(user)
    assert id is not None

    # Act
    actual = repository.get_by_telegram_username(TEST_TELEGRAM_USERNAME)

    # Assert
    assert actual is not None
    assert actual.telegram_username == TEST_TELEGRAM_USERNAME
    assert actual.access_level == 1
    assert actual.id is not None

    

    
