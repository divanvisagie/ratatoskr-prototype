import logging
import spacy_client

def test_question_is_about_code():
    assert spacy_client.question_is_about_code("How would I write a hello world in code?") == True

def test_is_youtube_video():
    assert (spacy_client.is_youtube_video("https://www.youtube.com/watch?v=h1K1mnitEx8")) == True
    assert (spacy_client.is_youtube_video("Could you watch this and tell me what it's about? https://www.youtube.com/watch?v=h1K1mnitEx8")) == True
    assert (spacy_client.is_youtube_video("https://en.wikipedia.org/wiki/Havi")) == False

if __name__ == '__main__':
    # Enable logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )