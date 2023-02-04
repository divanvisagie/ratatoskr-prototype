import spacy

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

    # Check if sentence contains a youtube link
    if any(token.text.lower().startswith("https://www.youtube.com/") for token in doc):
        return True

    # Check if the sentence contains specific keywords or phrases
    if any(token.text.lower() in ["youtube", "video"] for token in doc):
        return True
    
    return False