import logging
import spacy

from spacy.tokens import Token

logger = logging.getLogger(__name__)

# Load the English model
nlp = spacy.load("en_core_web_sm")

code_words = ["generate", "code", "program", "python", "javascript"]

def question_is_about_code(question: str) -> bool:
    doc = nlp(question)

    # Check if the sentence contains specific keywords or phrases
    if any(token.text.lower() in code_words for token in doc):
        return True
    
    return False


def is_youtube_video(question: str) -> bool:
    doc = nlp(question)

    # Print all the tokens
    for token in doc:
        logger.debug(f'TOKEN: {token}')

    # Check if sentence contains a youtube link
    if any(token.text.lower().startswith("https://www.youtube.com/") for token in doc):
        return True

    # Check if the sentence contains specific keywords or phrases
    if any(token.text.lower() in ["youtube", "video"] for token in doc):
        return True
    
    return False

def save_requested(question: str) -> bool:
    doc = nlp(question)
    for token in doc:
        if token.head.pos_ == "VERB" and token.head.text.lower() in ["save", "store", "remember", "keep"]:
            return True

    return False

def print_token_details(token: Token):
    logger.info(f'Text: {token.text}')
    logger.info(f'Lemma: {token.lemma_}')
    logger.info(f'POS: {token.pos_}')
    logger.info(f'Tag: {token.tag_}')
    logger.info(f'Dep: {token.dep_}')
    logger.info(f'Shape: {token.shape_}')
    logger.info(f'Is alpha: {token.is_alpha}')
    logger.info(f'Is stop: {token.is_stop}')