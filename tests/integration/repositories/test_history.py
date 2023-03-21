from repositories.history import HistoryRepository, NewHistory


def test_HistoryRepository_save_given_history_saves_history_to_database():
    # Arrange
    history = NewHistory(
        user_id=1,
        question="What is the meaning of life?",
        answer="42"
    )
    repository = HistoryRepository()

    # Act
    id = repository.save(history)

    # Assert
    assert id is not None
    actual = repository.get_by_id(id)

    for a in actual:
        assert a is not None
        assert a.question == "What is the meaning of life?"
        assert a.answer == "42"