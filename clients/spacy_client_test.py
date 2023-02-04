import unittest
import spacy_client


class TestSpacyClient(unittest.TestCase):
    def test_question_is_about_code(self):
        self.assertTrue(spacy_client.question_is_about_code("How would I write a hello world in python?"))

    def test_is_youtube_video(self):
        self.assertTrue(spacy_client.is_youtube_video("https://www.youtube.com/watch?v=h1K1mnitEx8"))
        self.assertFalse(spacy_client.is_youtube_video("https://en.wikipedia.org/wiki/Havi"))

if __name__ == '__main__':
    unittest.main()