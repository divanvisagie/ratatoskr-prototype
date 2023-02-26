
from functools import partial
import logging
import sys
#sys.path.append('../..') # move to root folder to import module from parent
from gpt2_model import GPT2Model

logger = logging.getLogger(__name__)


def get_completion_with_model(model, question: str) -> str:
    return model.complete(question)

def test_gpt2_model():
    model = GPT2Model()
    complete = partial(get_completion_with_model, model)
    complete("Question: What is the meaning of life?")
    actual = model.complete("What is the meaning of life?")
    expected = "42"
    logger.info(f"Actual: {actual}")
    # assert actual == expected

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    test_gpt2_model()