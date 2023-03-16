from unittest.mock import Mock

from filters.chat_gpt.filter import ChatGptCapability, build_context_from_history
from language_model.base_model import BaseModel
from language_model.gpt_chat_model import ChatGPTModel
from message_handler.message_types import RequestMessage
from repositories.history import History, HistoryRepository

MOCK_USER_ID = '1234-abcdef'
MOCK_ID = '1234-abcdef-1234'


def test_sets_prompt_on_create():
    """Test that we set the system prompt as soon as the filter is created"""
    model: BaseModel = Mock(spec=ChatGPTModel)
    repository: HistoryRepository = Mock(spec=HistoryRepository)
    ChatGptCapability([], model, repository)

    assert model.set_prompt.called == True


def test_reads_history_from_repository():
    """Test that we read the history from the repository"""
    model: ChatGPTModel = Mock(spec=ChatGPTModel)
    model.complete.return_value = '42'
    repository: HistoryRepository = Mock(spec=HistoryRepository)
    repository.get_last_n.return_value = []
    filter = ChatGptCapability([], model, repository)

    requestMessage: RequestMessage = RequestMessage(
        'What is the meaning of life?', MOCK_USER_ID)
    filter.apply(requestMessage)

    assert repository.get_last_n.called == True


def test_builds_context_from_history():
    repository: HistoryRepository = Mock(spec=HistoryRepository)
    repository.get_last_n.return_value = [
        History(MOCK_ID, '1234-abcdef', 'What is the meaning of life?', '42'),
        History(MOCK_ID, '1234-abcdef',
                'What is the meaning of the universe?', '43'),
        History(MOCK_ID, '1234-abcdef',
                'What is the meaning of everything?', '44'),
    ]
    actual = build_context_from_history(MOCK_USER_ID, repository)

    assert repository.get_last_n.called == True
    assert actual[0] == {'role': 'user',
                         'content': 'What is the meaning of life?'}
    assert actual[1] == {'role': 'assistant', 'content': '42'}
    assert actual[2] == {'role': 'user',
                         'content': 'What is the meaning of the universe?'}
    assert actual[3] == {'role': 'assistant', 'content': '43'}
    assert actual[4] == {'role': 'user',
                         'content': 'What is the meaning of everything?'}
    assert actual[5] == {'role': 'assistant', 'content': '44'}
