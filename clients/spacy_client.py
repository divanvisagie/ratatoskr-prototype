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
