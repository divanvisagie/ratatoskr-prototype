import openai
from os import environ

openai.api_key = TELEGRAM_BOT_TOKEN = environ['OPENAI_API_KEY']

model_engine = "text-davinci-003"

def get_answer(prompt):
    completion = openai.Completion.create(
        model=model_engine,
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completion.choices[0].text
    return message
