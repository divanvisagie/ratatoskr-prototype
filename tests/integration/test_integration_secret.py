import logging
from repositories.secret import NewSecret, SecretRepository, Secret

logger = create_logger__name__)

def test_save_secret():
    # Arrange
    repo = SecretRepository()
    
    # Act
    secret = NewSecret("user_id", "app_id", "question", "answer")
    id = repo.save(secret)
    actual = repo.get_by_id(id)

    # Assert
    assert actual.app_id == secret.app_id
    assert actual.user_id == secret.user_id
