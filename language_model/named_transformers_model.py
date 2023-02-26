import logging
from openai import Model
from transformers import pipeline, set_seed, GPT2LMHeadModel, GPT2Tokenizer
import torch
import sys
import os
from language_model.language_model import HUMAN_STOP_TOKEN


class NamedModel(Model):
    def __init__(self, model_name: str):
        self.model = pipeline('text-generation', model=model_name, do_sample=True)
        self.logger = logging.getLogger(__name__)

    def complete(self, question: str) -> str:
        response_text = self.model(question, max_length=1024, num_beams=1, num_return_sequences=1)[0]['generated_text']
        self.logger.info(f"Response text: {response_text}")
        response_text = response_text.split(question)[1] # extract the bot response from generated text
        response_text = response_text.split(f"{HUMAN_STOP_TOKEN}:")[0] # only grab until the next human input
        return response_text.strip()
