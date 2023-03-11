import logging
from named_model import SearchTermGenerator, QAPair

logger = logging.getLogger(__name__)

def test_search_term_generator_model():
    # Arrange
    model = SearchTermGenerator("gpt2")
    conversation = QAPair("What is the name of the actor library for scala?", "Akka")
    input = f"{str(conversation)}\nQuestion: what search term should i type in to get the documentation?\n Answer:"
    
    # Act
    actual = model.generate_for_context(input)

    # Assert
    assert actual == "Akka Documentation"


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )