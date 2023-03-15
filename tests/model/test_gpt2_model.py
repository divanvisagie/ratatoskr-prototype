import logging
from functools import partial

from language_model.gpt2_model import GPT2Model

logger = logging.getLogger(__name__)

def get_completion_with_model(model, question: str) -> str:
    return model.complete(question)

chat_prompt = """
Bot: Hello, how can I help you?
Human: What is the actor library for scala called?
Bot: 
"""

def test_gpt2_model():
    model = GPT2Model()
    complete = partial(get_completion_with_model, model)

    actual = complete(chat_prompt)
    logger.info(f"Actual: {actual}")

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    test_gpt2_model()