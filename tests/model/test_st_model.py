import logging

from language_model.search_term_generator.named_model import QAPair, SearchTermGenerator
from log_factory.logger import create_logger


logger = create_logger(__name__)

def test_search_term_generator_model():
    # Arrange
    model = SearchTermGenerator("gpt2")
    conversation = QAPair("What is the name of the actor library for scala?", "Akka")
    input = f"{str(conversation)}\nQuestion: what search term should i type in to get the documentation?\n Answer:"
    
    # Act
    actual = model.generate_for_context(input)

    # Assert
    assert actual == "Akka Documentation"
