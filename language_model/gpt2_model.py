import logging
import torch

from abc import ABC, abstractmethod

from transformers import pipeline, set_seed, GPT2LMHeadModel, GPT2Tokenizer

from language_model.language_model import LanguageModel


logger = logging.getLogger(__name__)

class GPT2Model (LanguageModel):
    def __init__(self):
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.logger = logging.getLogger(__name__)
        set_seed(32)
    
    def complete(self, question: str) -> str:
        input_ids = self.tokenizer.encode(question, return_tensors='pt')
        attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)
        output = self.model.generate(input_ids=input_ids, attention_mask=attention_mask, max_length=50, do_sample=True)
        output_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return output_text.strip()
    

