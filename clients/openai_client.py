import logging
import openai
from os import environ

openai.api_key = TELEGRAM_BOT_TOKEN = environ['OPENAI_API_KEY']

model_engine = "text-davinci-003"

logger = logging.getLogger(__name__)

def get_answer(prompt):
    try:
        logger.debug(f'Calling OpenAI completion with Prompt:\n{prompt}')
        completion = openai.Completion.create(
            model=model_engine,
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )
        logger.debug(f'Returned: {completion}')
        message = completion.choices[0].text
        return message
    except Exception as e:
        logger.error(f'Failed to get answer from OpenAI: {e}')
        return 'A trickster seems to have disabled the Bifrost! We cannot reach the library of the gods.'

