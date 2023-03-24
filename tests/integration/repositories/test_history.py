from repositories.history import HistoryRepository, NewHistory

USER_ID = "test_user_for_history_repository"

def test_HistoryRepository_get_last_n_gets_messages_in_order():
    # Arrange
    history = NewHistory(
        user_id=USER_ID,
        question="This is question 1",
        answer="This is an answer"
    )
    history2 = NewHistory(
        user_id=USER_ID,
        question="This is question 2",
        answer="This is an answer"
    )
    history3 = NewHistory(
        user_id=USER_ID,
        question="This is question 3",
        answer="This is an answer"
    )
    repository = HistoryRepository()

    # Act
    id = repository.save(history)
    id = repository.save(history2)
    id = repository.save(history3)

    # Assert
    assert id is not None
    returned_history_items = repository.get_last_n(USER_ID, 3)

    assert returned_history_items[0].question == "This is question 1"
    assert returned_history_items[1].question == "This is question 2"
    assert returned_history_items[2].question == "This is question 3"
    
    for a in returned_history_items:
        repository.delete(a.id) # Clean up        