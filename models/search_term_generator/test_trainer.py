"""
Following: https://huggingface.co/docs/transformers/tasks/question_answering
"""

import logging
from datasets import load_dataset


logger = logging.getLogger(__name__)

squad = load_dataset('squad',split="train[:5000]")

squad = squad.train_test_split(test_size=0.2)

s = squad["train"][0]






if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    logger.info(s)
