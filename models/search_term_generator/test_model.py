import logging
import os
import sys
import unittest
sys.path.insert(1, os.getcwd())
from model import SearchTermGenerator, QAPair

logger = logging.getLogger(__name__)

class TestSearchTermGeneratorModel(unittest.TestCase):
    def test_search_generator_model(self):
        # Arrange
        model = SearchTermGenerator("gpt2")
        conversation = QAPair("What is the name of the actor library for scala?", "Akka")
        input = f"{str(conversation)}\nQuestion: what search term should i type in to get the documentation?\n Answer:"
        
        # Act
        actual = model.generate_for_context(input)

        # Assert
        self.assertEqual(actual, "Akka Documentation")


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    unittest.main()