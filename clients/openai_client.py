import logging
import openai
from os import environ

from log_factory.logger import create_logger

openai.api_key = TELEGRAM_BOT_TOKEN = environ['OPENAI_API_KEY']

text_model = "text-davinci-003"
code_model = "code-davinci-002"

logger = create_logger(__name__)

HUMAN_STOP_TOKEN = "User"
AI_STOP_TOKEN = "Bot"

def get_text_answer(prompt):
    try:
        logger.debug(f'Calling OpenAI {text_model} completion with Prompt:\n{prompt}')
        completion = openai.Completion.create(
            model=text_model,
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=[HUMAN_STOP_TOKEN, AI_STOP_TOKEN],
            temperature=0.9,
        )
        logger.debug(f'Returned: {completion}')
        message = completion.choices[0].text
        return message
    except Exception as e:
        logger.error(f'Failed to get answer from OpenAI: {e}')
        return 'A trickster seems to have disabled the Bifrost! We cannot reach the library of the gods.'

def get_code_answer(prompt):
    try:
        logger.info(f'Calling OpenAI {code_model} completion with Prompt:\n{prompt}')
        completion = openai.Completion.create(
            model=code_model,
            prompt=prompt,
            max_tokens=256,
            n=1,
            temperature=0,
            top_p=1,
        )
        logger.debug(f'Returned: {completion}')
        message = completion.choices[0].text
        return f'```{message}```'
    except Exception as e:
        logger.error(f'Failed to get answer from OpenAI: {e}')
        return 'A trickster seems to have disabled the Bifrost! We cannot reach the library of the gods.'