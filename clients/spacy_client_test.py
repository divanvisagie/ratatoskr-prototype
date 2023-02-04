import unittest
import spacy_client


class TestSpacyClient(unittest.TestCase):
    def test_question_is_about_code(self):
        self.assertTrue(spacy_client.question_is_about_code("How would I write a hello world in python?"))


if __name__ == '__main__':
    unittest.main()