import logging
import torch

from transformers import set_seed, GPT2LMHeadModel, GPT2Tokenizer

from language_model.base_model import BaseModel
from log_factory.logger import create_logger


logger = create_logger(__name__)

class GPT2Model (BaseModel):
    def __init__(self):
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        set_seed(32)
    
    def complete(self, question: str) -> str:
        input_ids = self.tokenizer.encode(question, return_tensors='pt')
        attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)
        output = self.model.generate(input_ids=input_ids, attention_mask=attention_mask, max_length=250, do_sample=True)
        output_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return output_text.strip()
    


if __name__ == '__main__':
    model = GPT2Model()
    actual = model.complete("Bot: Hello, how can I help you?")