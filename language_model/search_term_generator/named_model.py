import logging
from transformers import pipeline, set_seed, GPT2LMHeadModel, GPT2Tokenizer

from log_factory.logger import create_logger

logger = create_logger(__name__)

class NamedModel(object):
    def __init__(self, model_name: str):
        self.model = pipeline('text-generation', model=model_name, do_sample=True)

    def ask_question(self, question: str) -> str:
        response_text = self.model(question, max_length=250, num_beams=1, num_return_sequences=1)[0]['generated_text']
        logger.info(f"Response text: {response_text}")
        response_text = response_text.split(question)[1] # extract the bot response from generated text
        response_text = response_text.split("Question:")[0] # only grab until the next human input
        return response_text.strip()


# #MODEL_NAME = "jordiclive/instruction-tuned-gpt-neox-20b"
# MODEL_NAME = "gpt2"
# #EleutherAI/gpt-j-6B
# #facebook/opt-125m

class QAPair():
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer

    def __str__(self):
        return f"Question: {self.question}\nAnswer: {self.answer}"

class SearchTermGenerator:
    def __init__(self, model_name: str):
        self.model = NamedModel(model_name)
        self.logger = create_logger(__name__)
        prompt_history = [
            QAPair("What is the most popular http library for rust?", "Axios"),
            QAPair("What search term should i type in to get the documentation?", "Axios Documentation"),
            QAPair("What is the most popular http library for python?", "Requests"),
            QAPair("What search term should i type in to get the documentation?", "Requests Documentation"),
            QAPair("What is a good http library for javascript?", "Expressjs"),
            QAPair("What search term should i type in to get the documentation?", "Expressjs Documentation"),
        ]
        self.prompt  = "\n".join([str(qa) for qa in prompt_history])
        self.logger.info(f"Initializing with Prompt: {self.prompt}")

    def generate_for_context(self, question: str) -> str:
        full_input = self.prompt + question
        return self.model.ask_question(full_input)


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
   
    logger = create_logger(__name__)
    conversation = QAPair("What is the name of the actor library for scala?", "Akka")

    input = f"{str(conversation)}\nQuestion: what search term should i type in to get the documentation?\n Answer:"

    model = SearchTermGenerator("gpt2")
    answer = model.generate_for_context(conversation)
    logger.info(f'Search term: {answer}')