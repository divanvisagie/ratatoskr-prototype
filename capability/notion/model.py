import spacy

nlp = spacy.load("en_core_web_sm")

def save_requested(question: str) -> float:
    doc = nlp(question)
    for token in doc:
        if token.head.pos_ == "VERB" and token.head.text.lower() in ["save", "store", "remember", "keep"]:
            return 1.0
    return 0.0