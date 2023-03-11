import logging
import openai

from language_model.base_model import BaseModel

logger = logging.getLogger(__name__)

class ChatGPTModel (BaseModel):
    def __init__(self, system_prompt: str):
        self.system_prompt = { "role": "system", "content": system_prompt }
    
    def complete(self, prompt: str) -> str:
        completion =  openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                self.system_prompt,
                { "role": "user", "content": prompt },
            ]
        )
        return completion.choices[0].message.content
        
if __name__ == "__main__":
    model = ChatGPTModel("You are ChatGPT, a large language model trained by OpenAI. You answer questions and when the user asks code questions, you will answer with code examples in markdown format.")
    completion = model.complete("How do I write a fastAPI program in python?")
    print(completion)