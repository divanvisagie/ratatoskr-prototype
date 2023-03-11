import logging
from filter import DuckDuckFilter
from message_handler.message_types import RequestMessage

positive_sentences = [
    "Do you have documentation for this?",
    "Can you find the documentation?",
    "I don't know the answer to that, but I'm sure a quick search on the internet or asking a fellow raven who may be more knowledgeable on the subject will help you find the answer you seek. Good luck!",
]

def test_applies_to():
    filter = DuckDuckFilter()
    for sentence in positive_sentences:
        msg = RequestMessage(
            sentence, 
            1
        )
        actual = filter.applies_to(msg)
        assert actual == True

def test_applies_to_negative():
    filter = DuckDuckFilter()
    msg = RequestMessage(
        "Save that", 
        1
    )
    actual = filter.applies_to(msg)
    assert actual == False

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )


