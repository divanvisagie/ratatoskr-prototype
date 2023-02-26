import logging
import os
import sys
from functools import partial

# relative imports
sys.path.insert(1, os.getcwd())
from gpt2_model import GPT2Model
from named_transformers_model import NamedModel
from base_model import HUMAN_STOP_TOKEN
from repositories.history import build_context_from_history
#sys.path.append('../..') # move to root folder to import module from parent

logger = logging.getLogger(__name__)

def get_completion_with_model(model, question: str) -> str:
    return model.complete(question)

def test_gpt2_model():
    model = NamedModel("gpt2")
    complete = partial(get_completion_with_model, model)

    user_question = "What are the different kinds of potatoes?"

    # build up context
    history_context = build_context_from_history(0)
    #logger.info(f"History context: {history_context}")
    
    prompt = f"{history_context}\n{HUMAN_STOP_TOKEN}: {user_question}"

    actual = complete(prompt)
    logger.info(f"Actual: {actual}")
    # assert actual == expected

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    test_gpt2_model()